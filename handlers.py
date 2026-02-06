"""Message matchers for Spud bot. Each function takes message text, returns bool."""

import re

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
