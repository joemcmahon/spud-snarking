"""Message matchers for Spud bot. Each function takes message text, returns bool."""

import random
import re
from enum import Enum, auto

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
