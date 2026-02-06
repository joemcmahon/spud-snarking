import pytest
from handlers import (
    matches_oblique,
    matches_greeting,
    matches_goodnight,
    matches_thanks,
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
