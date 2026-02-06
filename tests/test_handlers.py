import pytest
from unittest.mock import patch
from handlers import (
    matches_oblique,
    matches_greeting,
    matches_goodnight,
    matches_thanks,
    dispatch,
    MatchResult,
)


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

    @patch("handlers.random.random", return_value=0.50)
    def test_thanks_with_mention(self, mock_rand):
        result = dispatch("thanks spud", is_mentioned=True)
        assert result == MatchResult.THANKS

    @patch("handlers.random.random", return_value=0.50)
    def test_catchall_with_mention_no_match(self, mock_rand):
        result = dispatch("you're weird spud", is_mentioned=True)
        assert result == MatchResult.SNARK

    def test_no_mention_no_oblique_returns_none(self):
        result = dispatch("just chatting about stuff", is_mentioned=False)
        assert result is None

    @patch("handlers.random.random", return_value=0.95)
    def test_thanks_still_fires_under_threshold(self, mock_rand):
        result = dispatch("thanks spud", is_mentioned=True)
        assert result == MatchResult.THANKS

    @patch("handlers.random.random", side_effect=[0.99, 0.50])
    def test_thanks_blocked_by_probability(self, mock_rand):
        result = dispatch("thanks spud", is_mentioned=True)
        # 0.99 > 0.98, thanks blocked, falls through to snark (0.50 < 0.90)
        assert result == MatchResult.SNARK

    @patch("handlers.random.random", return_value=0.95)
    def test_snark_blocked_by_probability(self, mock_rand):
        result = dispatch("you're weird spud", is_mentioned=True)
        # 0.95 > 0.90, snark blocked
        assert result is None
