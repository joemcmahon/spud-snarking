# Spud Snarking Bot — Design

## Overview

A standalone Python Discord bot that recreates Spud's personality from the old Radiospiral Slack bot. Spud passively monitors channels for Oblique Strategy trigger words and responds to @mentions/DMs with snarky, flippant-but-endearing personality.

Separate process from the Now Playing bot. Uses an already-registered idle Discord bot account for Spud.

## Architecture

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
├── requirements-dev.txt
└── tests/
    └── test_handlers.py
```

**Dependencies:** `discord.py`, `pyyaml`, `python-dotenv`

**Message flow:** Bot connects, listens via `on_message`, messages run through priority-ordered matcher chain, first match handles the response.

## Matcher Chain

Priority order (first match wins):

### 1. Oblique Strategies — passive, all channels
- Pattern: `\boblique\b|\bstrateg(?:y|ies)\b`
- Probability: 100%
- No @mention needed

### 2. Greetings — mention/DM only
- Pattern: `\b(?:hi|hey|hoi|yo|hai|hello|howdy|greetings|sup|good\s+(?:morning|day|afternoon|evening))\b`
- Probability: 100%

### 3. Goodnight — mention/DM only
- Pattern: `\b(?:bye|nite|night|later|vista|goodbye|dreams|see\s+you|bai|good\s*night|ttfn|syl|nini)\b`
- Probability: 100%

### 4. Thanks — mention/DM only
- Pattern: `\bthanks?\b|\bthanky?\b|\bthankies\b|\bcheers\b|\bty\b`
- Probability: 98%

### 5. Catch-all snark — mention/DM only
- No pattern (fires if nothing else matched)
- Probability: 90%

Bot ignores its own messages. Probabilities are constants at the top of the script for easy tuning.

## Response Files

All response pools are YAML lists in `data/`. Loaded once at startup.

### data/greetings.yml
```yaml
- "hi there, how are you?"
- "Heya, how's you?"
- "sup dude"
- "yo wassup"
- "oh hey"
- "well well well, look who it is"
- "hiiiii"
- "what's good?"
- "ah, my favorite human. maybe."
```

### data/goodnight.yml
```yaml
- "nini..."
- "sweet dreams"
- "see you soon?"
- "take it easy then"
- "cheers mate"
- "don't let the bits bite"
- "I'll just be here. in the dark. alone."
- "later, meatbag"
- "zzz"
```

### data/thanks.yml
```yaml
- "No problem!"
- "You're welcome!"
- "Happy to help!"
- "de nada!"
- "My pleasure!"
- "yeah yeah"
- "I know, I'm amazing"
- "cool"
- "don't mention it. seriously."
```

### data/snark.yml
```yaml
- "word."
- "Did you say something?"
- "I'm going to pretend I didn't hear that"
- "noted."
- "fascinating. truly."
- "sorry, I was napping"
- "that's nice dear"
- "that's nice dear"
- "I have opinions about this but I'll keep them to myself. for now."
- "beep boop or whatever"
```

### data/strategies.yml
Copied from https://github.com/joemcmahon/mrspiral-spudtest/blob/master/strategies.yml

## Docker & Deployment

### Dockerfile
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

### docker-compose.yml
```yaml
services:
  spud:
    build: .
    env_file: .env
    restart: unless-stopped
```

### .env.example
```
DISCORD_BOT_TOKEN=your-token-here
```

### Discord Bot Setup
- **Gateway Intents**: `message_content` must be toggled ON in Discord Developer Portal
- **Bot Permissions**: Send Messages, Read Message History
- Spud must be invited to channels where he should be active

### requirements.txt
```
discord.py>=2.3,<3
pyyaml>=6.0
python-dotenv>=1.0
```

## Testing

**Framework:** pytest (in `requirements-dev.txt`)

**What to test:**
- Matcher functions: regex matches/rejects correctly (pure functions, text in, bool out)
- Response loader: reads YAML, handles missing files
- Probability logic: with seeded random, correct skip behavior
- Priority order: "hey Spud, what's your strategy?" triggers oblique, not greetings
- Self-ignore: bot doesn't respond to own messages

**What NOT to test:**
- Discord API integration (discord.py's job)
- Bot connection/authentication

## References
- Old Spud bot: https://github.com/joemcmahon/mrspiral-spudtest/
- Oblique Strategies source: https://github.com/joemcmahon/mrspiral-spudtest/blob/master/strategies.yml
