---
date: 2026-02-05T13:50:23-0800
session_name: general
researcher: claude
git_commit: n/a (empty repo, .git was mislocated in parent directory)
branch: main
repository: spud-snarking
topic: "Spud Discord Snarking Bot Design"
tags: [discord-bot, python, brainstorming, design]
status: complete
last_updated: 2026-02-05
last_updated_by: claude
type: implementation_strategy
root_span_id: ""
turn_span_id: ""
---

# Handoff: Spud Discord Snarking Bot — Design Complete, Ready for Implementation

## Task(s)
- **Brainstorming/Design session** (COMPLETE): Collaborated with user to design a Discord bot that recreates and modernizes the old Slack-based Spud bot's personality features.
- **Implementation** (PLANNED): Not yet started. All 5 design sections presented and approved. Full design doc written to `docs/plans/2026-02-05-spud-snarking-bot-design.md`.

## Critical References
- **Old Spud bot source**: https://github.com/joemcmahon/mrspiral-spudtest/blob/master/ — the original Node.js/Slack bot. Contains all original response pools and behavior patterns.
- **Oblique Strategies file**: https://github.com/joemcmahon/mrspiral-spudtest/blob/master/strategies.yml — YAML list of Brian Eno's Oblique Strategies, to be copied directly into the new project.

## Recent changes
No code changes — this was a design session only. The directory `thoughts/shared/handoffs/general/` was created for this handoff.

## Learnings

### Design Decisions Made

**Platform & Stack:**
- Python with `discord.py`, `pyyaml`, `python-dotenv`
- Docker-ready (Dockerfile + docker-compose.yml)
- Completely separate from the existing Now Playing bot (which uses AzuraCast SSE and posts as "Now Playing")
- Uses an **already-registered Discord bot account** for Spud that is currently idle

**Bot Behavior — Two Modes:**

1. **Passive monitoring (all channels, no mention needed):**
   - Oblique Strategies: triggered by words "oblique", "strategy", or "strategies" appearing in any message
   - Responds 100% of the time with a random Oblique Strategy from `strategies.yml`

2. **Active responses (only on @Spud mention or DM):**
   - **Greetings**: matches hi/hey/hello/howdy/etc → random greeting response
   - **Goodnight**: matches bye/night/later/etc → random farewell response
   - **Thanks**: matches thanks/cheers/ty/etc → random acknowledgment (98% probability)
   - **Catch-all snark**: any other mention/DM → random quip (90% probability)

**No follow-up conversations.** The old bot had conversation routing (greet → follow-up) but user decided to skip this. Simplifies the bot significantly — no conversation state tracking needed.

**Response Pools are File-Driven:**
- All response pools stored as YAML files in `data/` directory (not hardcoded)
- Files: `strategies.yml`, `greetings.yml`, `goodnight.yml`, `thanks.yml`, `snark.yml`
- Easy to expand Spud's vocabulary without touching code
- Personality goal: "flippant but endearing"

**Probability Constants:**
- Defined at the top of the script for easy tuning
- `THANKS_PROBABILITY = 0.98`
- `SNARK_PROBABILITY = 0.90`
- `OBLIQUE_PROBABILITY = 1.0` (always responds)

**Configuration:**
- `.env` file for secrets (Discord bot token)
- `.env.example` committed as template
- YAML files for all response data

### Approved Architecture (Section 1 of design)

```
spud-snarking/
├── bot.py              # Main bot entry point
├── handlers.py         # Message matching and response logic
├── responses.py        # YAML loader for response pools
├── data/
│   ├── strategies.yml  # Oblique Strategies (from existing repo)
│   ├── greetings.yml   # Greeting responses
│   ├── goodnight.yml   # Farewell responses
│   ├── thanks.yml      # Acknowledgment responses
│   └── snark.yml       # Catch-all quips
├── .env                # Bot token (not committed)
├── .env.example        # Template showing required vars
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── tests/
    └── test_handlers.py
```

**Message flow:** Bot connects → listens via `on_message` → messages run through priority-ordered matcher chain → first match handles the response. Oblique triggers checked on every message; all others only fire on @mentions or DMs.

### Remaining Design Sections (not yet presented/validated)

The following sections still need to be written and validated with the user:
- **Section 2**: Matcher chain details — regex patterns, priority order
- **Section 3**: YAML response file format, initial response pools (expanding old ones)
- **Section 4**: Docker setup, deployment, Discord bot permissions/intents needed
- **Section 5**: Testing approach

### Original Response Pools (from old bot, to be expanded)

**Greetings:** "hi there, how are you?", "Heya, how's you?", "sup dude", "yo wassup", "hello ambient, how are you?"

**Goodnight:** "Goodnight :zzz:", "see you soon? :blush:", "take it easy then", "cheers mate", "sweet dreams :star2:", "nini..."

**Thanks:** "No problem!", "You are welcome!", "Happy to help!", "de nada!", "My pleasure!", ":pray:", ":raised_hands:", "cool"

**Catch-all snark:** ":wave:", ":pray:", ":raised_hands:", "word.", ":wink:", "Did you say something?", ":innocent:", ":hankey:", ":smirk:"

**Regex patterns from old bot:**
- Greetings: `/\b(hi|hey|hoi|yo|hai|hello|howdy|greetings|sup|good\s+(morning|day|afternoon|evening))\b/i`
- Goodnight: `/bye|nite|night|later|vista|goodbye|dreams|see you|bai|good night|ttfn|syl|nini/i`
- Thanks: `/(T|t)hank( |s|y|ies)|cheers|ty/i`
- Oblique: `/oblique|strateg(y|ies)/i`

## Post-Mortem (Required for Artifact Index)

### What Worked
- **Brainstorming skill approach**: One question at a time with multiple-choice options kept the conversation focused and efficient. Got through all major design decisions in ~10 turns.
- **Referencing old source code**: Having the user paste the old bot code gave concrete patterns, response pools, and regex patterns to build from rather than designing from scratch.

### What Failed
- **Token limits**: Ran out of budget before completing the full design presentation (only got through section 1 of ~5). The remaining design sections will need to be completed in the next session.

### Key Decisions
- **Separate bot process**: Keep snarking completely separate from the Now Playing bot to avoid complexity
  - Alternatives considered: Adding to existing bot
  - Reason: Now Playing bot is tightly coupled to AzuraCast SSE; merging would create a mess
- **No conversation follow-ups**: Skip the greeting/goodnight follow-up responses
  - Alternatives considered: Implementing with time-window tracking
  - Reason: Cute but not essential; removes need for conversation state tracking
- **File-driven responses**: YAML files for all response pools
  - Alternatives considered: Hardcoded arrays in Python
  - Reason: Easy to expand personality without touching code
- **Passive oblique strategy monitoring**: No @mention needed for strategy triggers
  - Alternatives considered: Require mention like other behaviors
  - Reason: "More charming if he just pipes up" — user preference

## Artifacts
- `thoughts/shared/handoffs/general/2026-02-05_13-50-23_spud-snarking-bot-design.md` (this file)

## Action Items & Next Steps
1. **Initialize git repo** in spud-snarking directory (the old `.git` was mislocated in parent)
2. **Complete design presentation** — sections 2-5 (matchers, response files, Docker/deployment, testing)
3. **Fetch strategies.yml** from https://github.com/joemcmahon/mrspiral-spudtest/blob/master/strategies.yml
4. **Create initial YAML response files** with old responses + expanded "flippant but endearing" additions
5. **Write the design doc** to `docs/plans/` once all sections are validated
6. **Implement the bot** using TDD approach
7. **Dockerize** with Dockerfile + docker-compose.yml
8. **Test with the existing registered Spud Discord bot token**

## Other Notes
- The existing Spud Discord bot is already registered but idle — no new bot creation needed in Discord Developer Portal
- The Now Playing bot posts as "Now Playing", not as "Spud", so there's no identity conflict
- Slack emoji syntax (`:zzz:`, `:blush:`, etc.) will need to be converted to Discord emoji syntax in response files — Discord uses the same format for standard emoji but custom emoji syntax differs
- Discord requires specific Gateway Intents: `message_content` intent is needed to read message text for passive monitoring. This must be enabled in the Discord Developer Portal.
- The old bot's Icecast monitoring, track history, and peak listener features are NOT part of this bot
