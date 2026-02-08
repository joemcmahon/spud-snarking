# Spud Snarking Bot Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Python Discord bot that monitors channels for Oblique Strategy triggers and responds to @mentions/DMs with snarky personality.

**Architecture:** Single-process bot using discord.py. Messages flow through a priority-ordered matcher chain (oblique > greetings > goodnight > thanks > catch-all snark). Response pools are YAML files loaded at startup. Dockerized for deployment.

**Tech Stack:** Python 3.12, discord.py, pyyaml, python-dotenv, pytest

**Design doc:** `docs/plans/2026-02-05-spud-snarking-bot-design.md`

---

### Task 1: Project Scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `requirements-dev.txt`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `.python-version`

**Step 1: Create requirements.txt**

```
discord.py>=2.3,<3
pyyaml>=6.0
python-dotenv>=1.0
```

**Step 2: Create requirements-dev.txt**

```
-r requirements.txt
pytest>=8.0
```

**Step 3: Create .env.example**

```
DISCORD_BOT_TOKEN=your-token-here
```

**Step 4: Create .gitignore**

```
__pycache__/
*.pyc
.env
.venv/
venv/
```

**Step 5: Create .python-version**

```
3.12
```

**Step 6: Install dependencies**

Run: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements-dev.txt`
Expected: All packages install successfully

**Step 7: Commit**

```bash
git add requirements.txt requirements-dev.txt .env.example .gitignore .python-version
git commit -m "feat: project scaffolding with dependencies"
```

---

### Task 2: Response Pool Loader

**Files:**
- Create: `responses.py`
- Create: `tests/test_responses.py`
- Create: `tests/__init__.py`

**Step 1: Write the failing tests**

```python
# tests/test_responses.py
import os
import pytest
from responses import load_pool, get_random


@pytest.fixture
def sample_yaml(tmp_path):
    """Create a temporary YAML file with test data."""
    p = tmp_path / "test_pool.yml"
    p.write_text('- "alpha"\n- "bravo"\n- "charlie"\n')
    return str(p)


@pytest.fixture
def empty_yaml(tmp_path):
    """Create an empty YAML file."""
    p = tmp_path / "empty.yml"
    p.write_text("---\n")
    return str(p)


def test_load_pool_returns_list(sample_yaml):
    pool = load_pool(sample_yaml)
    assert pool == ["alpha", "bravo", "charlie"]


def test_load_pool_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_pool("/nonexistent/path.yml")


def test_load_pool_empty_file_returns_empty_list(empty_yaml):
    pool = load_pool(empty_yaml)
    assert pool == []


def test_get_random_returns_item_from_pool():
    pool = ["alpha", "bravo", "charlie"]
    result = get_random(pool)
    assert result in pool


def test_get_random_empty_pool_returns_none():
    result = get_random([])
    assert result is None
```

**Step 2: Run tests to verify they fail**

Run: `source .venv/bin/activate && pytest tests/test_responses.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'responses'`

**Step 3: Write minimal implementation**

```python
# responses.py
"""YAML response pool loader for Spud bot."""

import random
from pathlib import Path

import yaml


def load_pool(filepath: str) -> list[str]:
    """Load a YAML list from a file. Returns list of strings."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Response pool not found: {filepath}")
    with open(path) as f:
        data = yaml.safe_load(f)
    if data is None:
        return []
    return data


def get_random(pool: list[str]) -> str | None:
    """Return a random item from a pool, or None if empty."""
    if not pool:
        return None
    return random.choice(pool)
```

**Step 4: Run tests to verify they pass**

Run: `source .venv/bin/activate && pytest tests/test_responses.py -v`
Expected: All 5 tests PASS

**Step 5: Commit**

```bash
git add responses.py tests/__init__.py tests/test_responses.py
git commit -m "feat: YAML response pool loader with tests"
```

---

### Task 3: YAML Data Files

**Files:**
- Create: `data/strategies.yml` (fetched from GitHub)
- Create: `data/greetings.yml`
- Create: `data/goodnight.yml`
- Create: `data/thanks.yml`
- Create: `data/snark.yml`

**Step 1: Fetch strategies.yml from existing repo**

Run: `mkdir -p data && gh api repos/joemcmahon/mrspiral-spudtest/contents/strategies.yml --jq '.content' | base64 -d > data/strategies.yml`
Expected: File created with ~183 lines of Oblique Strategies

**Step 2: Create data/greetings.yml**

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

**Step 3: Create data/goodnight.yml**

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

**Step 4: Create data/thanks.yml**

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

**Step 5: Create data/snark.yml**

```yaml
- "word."
- "Did you say something?"
- "I'm going to pretend I didn't hear that"
- "noted."
- "fascinating. truly."
- "sorry, I was napping"
- "that's nice dear"
- "I have opinions about this but I'll keep them to myself. for now."
- "beep boop or whatever"
```

**Step 6: Verify all files load**

Run: `source .venv/bin/activate && python -c "from responses import load_pool; [print(f'{f}: {len(load_pool(f\"data/{f}\"))} items') for f in ['strategies.yml','greetings.yml','goodnight.yml','thanks.yml','snark.yml']]"`
Expected: Each file prints its item count

**Step 7: Commit**

```bash
git add data/
git commit -m "feat: add response pool YAML data files"
```

---

### Task 4: Matcher Functions (Handlers)

**Files:**
- Create: `handlers.py`
- Create: `tests/test_handlers.py`

**Step 1: Write the failing tests**

```python
# tests/test_handlers.py
import pytest
from handlers import (
    matches_oblique,
    matches_greeting,
    matches_goodnight,
    matches_thanks,
)


# --- Oblique Strategy matcher ---

class TestMatchesOblique:
    def test_matches_strategy(self):
        assert matches_oblique("what's your strategy?")

    def test_matches_strategies(self):
        assert matches_oblique("any good strategies?")

    def test_matches_oblique(self):
        assert matches_oblique("try an oblique approach")

    def test_rejects_strategic(self):
        assert not matches_oblique("strategic planning meeting")

    def test_rejects_unrelated(self):
        assert not matches_oblique("hello there")

    def test_case_insensitive(self):
        assert matches_oblique("OBLIQUE Strategies")


# --- Greeting matcher ---

class TestMatchesGreeting:
    def test_matches_hi(self):
        assert matches_greeting("hi spud")

    def test_matches_hello(self):
        assert matches_greeting("hello there")

    def test_matches_good_morning(self):
        assert matches_greeting("good morning everyone")

    def test_matches_sup(self):
        assert matches_greeting("sup")

    def test_matches_howdy(self):
        assert matches_greeting("howdy partner")

    def test_rejects_unrelated(self):
        assert not matches_greeting("what is the track?")

    def test_rejects_highway(self):
        assert not matches_greeting("take the highway")


# --- Goodnight matcher ---

class TestMatchesGoodnight:
    def test_matches_goodnight(self):
        assert matches_goodnight("good night everyone")

    def test_matches_bye(self):
        assert matches_goodnight("bye spud")

    def test_matches_nini(self):
        assert matches_goodnight("nini")

    def test_matches_ttfn(self):
        assert matches_goodnight("ttfn!")

    def test_matches_see_you(self):
        assert matches_goodnight("see you later")

    def test_rejects_unrelated(self):
        assert not matches_goodnight("what time is it?")


# --- Thanks matcher ---

class TestMatchesThanks:
    def test_matches_thanks(self):
        assert matches_thanks("thanks spud")

    def test_matches_thank(self):
        assert matches_thanks("thank you")

    def test_matches_cheers(self):
        assert matches_thanks("cheers mate")

    def test_matches_ty(self):
        assert matches_thanks("ty!")

    def test_rejects_unrelated(self):
        assert not matches_thanks("play something good")
```

**Step 2: Run tests to verify they fail**

Run: `source .venv/bin/activate && pytest tests/test_handlers.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'handlers'`

**Step 3: Write minimal implementation**

```python
# handlers.py
"""Message matchers for Spud bot. Each function takes message text, returns bool."""

import re

# Compiled regex patterns for performance
_OBLIQUE_RE = re.compile(r"\boblique\b|\bstrateg(?:y|ies)\b", re.IGNORECASE)
_GREETING_RE = re.compile(
    r"\b(?:hi|hey|hoi|yo|hai|hello|howdy|greetings|sup"
    r"|good\s+(?:morning|day|afternoon|evening))\b",
    re.IGNORECASE,
)
_GOODNIGHT_RE = re.compile(
    r"\b(?:bye|nite|night|later|vista|goodbye|dreams"
    r"|see\s+you|bai|good\s*night|ttfn|syl|nini)\b",
    re.IGNORECASE,
)
_THANKS_RE = re.compile(
    r"\bthanks?\b|\bthanky?\b|\bthankies\b|\bcheers\b|\bty\b",
    re.IGNORECASE,
)


def matches_oblique(text: str) -> bool:
    return bool(_OBLIQUE_RE.search(text))


def matches_greeting(text: str) -> bool:
    return bool(_GREETING_RE.search(text))


def matches_goodnight(text: str) -> bool:
    return bool(_GOODNIGHT_RE.search(text))


def matches_thanks(text: str) -> bool:
    return bool(_THANKS_RE.search(text))
```

**Step 4: Run tests to verify they pass**

Run: `source .venv/bin/activate && pytest tests/test_handlers.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add handlers.py tests/test_handlers.py
git commit -m "feat: message matcher functions with tests"
```

---

### Task 5: Priority Dispatcher

**Files:**
- Modify: `handlers.py` (add `dispatch` function)
- Modify: `tests/test_handlers.py` (add dispatch tests)

This task adds the priority-ordered dispatch function that determines which matcher wins.

**Step 1: Write the failing tests**

Append to `tests/test_handlers.py`:

```python
from unittest.mock import patch
from handlers import dispatch, MatchResult


class TestDispatch:
    def test_oblique_wins_over_greeting(self):
        """'hey, what's your strategy?' should trigger oblique, not greeting."""
        result = dispatch("hey, what's your strategy?", is_mentioned=True)
        assert result == MatchResult.OBLIQUE

    def test_oblique_fires_without_mention(self):
        result = dispatch("try a different strategy", is_mentioned=False)
        assert result == MatchResult.OBLIQUE

    def test_greeting_requires_mention(self):
        result = dispatch("hello everyone", is_mentioned=False)
        assert result is None

    def test_greeting_with_mention(self):
        result = dispatch("hello spud", is_mentioned=True)
        assert result == MatchResult.GREETING

    def test_goodnight_with_mention(self):
        result = dispatch("goodnight spud", is_mentioned=True)
        assert result == MatchResult.GOODNIGHT

    def test_thanks_with_mention(self):
        result = dispatch("thanks spud", is_mentioned=True)
        assert result == MatchResult.THANKS

    def test_catchall_with_mention_no_match(self):
        result = dispatch("you're weird spud", is_mentioned=True)
        assert result == MatchResult.SNARK

    def test_no_mention_no_oblique_returns_none(self):
        result = dispatch("just chatting about stuff", is_mentioned=False)
        assert result is None

    @patch("handlers.random.random", return_value=0.95)
    def test_thanks_skipped_by_probability(self, mock_rand):
        result = dispatch("thanks spud", is_mentioned=True)
        # 0.95 > THANKS_PROBABILITY (0.98) is false, so it should still fire
        # Actually 0.95 < 0.98, so thanks fires
        assert result == MatchResult.THANKS

    @patch("handlers.random.random", return_value=0.99)
    def test_thanks_blocked_by_probability(self, mock_rand):
        result = dispatch("thanks spud", is_mentioned=True)
        # 0.99 > 0.98, thanks blocked, falls through to snark
        assert result == MatchResult.SNARK

    @patch("handlers.random.random", return_value=0.95)
    def test_snark_blocked_by_probability(self, mock_rand):
        result = dispatch("you're weird spud", is_mentioned=True)
        # 0.95 > 0.90, snark blocked
        assert result is None
```

**Step 2: Run tests to verify they fail**

Run: `source .venv/bin/activate && pytest tests/test_handlers.py::TestDispatch -v`
Expected: FAIL — `ImportError: cannot import name 'dispatch'`

**Step 3: Write minimal implementation**

Add to `handlers.py`:

```python
import random
from enum import Enum, auto


# Probability constants — tune these to adjust Spud's chattiness
OBLIQUE_PROBABILITY = 1.0
GREETING_PROBABILITY = 1.0
GOODNIGHT_PROBABILITY = 1.0
THANKS_PROBABILITY = 0.98
SNARK_PROBABILITY = 0.90


class MatchResult(Enum):
    OBLIQUE = auto()
    GREETING = auto()
    GOODNIGHT = auto()
    THANKS = auto()
    SNARK = auto()


def dispatch(text: str, is_mentioned: bool) -> MatchResult | None:
    """Run text through matcher chain in priority order. Returns match type or None."""
    # 1. Oblique — passive, no mention needed
    if matches_oblique(text) and random.random() < OBLIQUE_PROBABILITY:
        return MatchResult.OBLIQUE

    # Everything below requires mention/DM
    if not is_mentioned:
        return None

    # 2. Greeting
    if matches_greeting(text) and random.random() < GREETING_PROBABILITY:
        return MatchResult.GREETING

    # 3. Goodnight
    if matches_goodnight(text) and random.random() < GOODNIGHT_PROBABILITY:
        return MatchResult.GOODNIGHT

    # 4. Thanks
    if matches_thanks(text) and random.random() < THANKS_PROBABILITY:
        return MatchResult.THANKS

    # 5. Catch-all snark
    if random.random() < SNARK_PROBABILITY:
        return MatchResult.SNARK

    return None
```

**Step 4: Run tests to verify they pass**

Run: `source .venv/bin/activate && pytest tests/test_handlers.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add handlers.py tests/test_handlers.py
git commit -m "feat: priority dispatcher with probability constants"
```

---

### Task 6: Discord Bot Core

**Files:**
- Create: `bot.py`

This task wires everything together with the discord.py client. No automated tests — this is the integration layer.

**Step 1: Create bot.py**

```python
# bot.py
"""Spud Snarking Bot — Discord personality bot for Radiospiral."""

import os
from pathlib import Path

import discord
from dotenv import load_dotenv

from handlers import MatchResult, dispatch
from responses import get_random, load_pool

load_dotenv()

DATA_DIR = Path(__file__).parent / "data"

# Load all response pools at startup
POOLS = {
    MatchResult.OBLIQUE: load_pool(DATA_DIR / "strategies.yml"),
    MatchResult.GREETING: load_pool(DATA_DIR / "greetings.yml"),
    MatchResult.GOODNIGHT: load_pool(DATA_DIR / "goodnight.yml"),
    MatchResult.THANKS: load_pool(DATA_DIR / "thanks.yml"),
    MatchResult.SNARK: load_pool(DATA_DIR / "snark.yml"),
}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Spud is lurking as {client.user}")


@client.event
async def on_message(message: discord.Message):
    # Never respond to ourselves
    if message.author == client.user:
        return

    text = message.content
    is_mentioned = (
        client.user in message.mentions
        or isinstance(message.channel, discord.DMChannel)
    )

    result = dispatch(text, is_mentioned)
    if result is None:
        return

    response = get_random(POOLS[result])
    if response:
        await message.channel.send(response)


def main():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("Error: DISCORD_BOT_TOKEN not set in .env")
        raise SystemExit(1)
    client.run(token)


if __name__ == "__main__":
    main()
```

**Step 2: Verify it loads without errors (no token needed)**

Run: `source .venv/bin/activate && python -c "import bot; print('bot module loads OK')"`
Expected: Prints "bot module loads OK" (may warn about missing token, that's fine)

**Step 3: Commit**

```bash
git add bot.py
git commit -m "feat: Discord bot core wiring handlers and responses"
```

---

### Task 7: Docker Setup

**Files:**
- Create: `Dockerfile`
- Create: `docker-compose.yml`

**Step 1: Create Dockerfile**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

**Step 2: Create docker-compose.yml**

```yaml
services:
  spud:
    build: .
    env_file: .env
    restart: unless-stopped
```

**Step 3: Verify Docker build**

Run: `docker build -t spud-snarking .`
Expected: Image builds successfully

**Step 4: Commit**

```bash
git add Dockerfile docker-compose.yml
git commit -m "feat: Docker setup for deployment"
```

---

### Task 8: Final Verification

**Step 1: Run full test suite**

Run: `source .venv/bin/activate && pytest tests/ -v`
Expected: All tests PASS

**Step 2: Verify Docker build is clean**

Run: `docker build -t spud-snarking .`
Expected: Builds with no warnings

**Step 3: Final commit (if any cleanup needed)**

Only if there are changes from verification.

---

## Post-Implementation Notes

**To run locally:** Create `.env` with your Discord bot token, then `python bot.py`

**To deploy:** `docker compose up -d`

**Discord Developer Portal setup required:**
1. Go to the Spud bot application
2. Under Bot settings, enable "Message Content Intent"
3. Generate invite URL with permissions: Send Messages, Read Message History
4. Invite Spud to desired channels

**To add more responses:** Edit the YAML files in `data/` and restart the bot.
