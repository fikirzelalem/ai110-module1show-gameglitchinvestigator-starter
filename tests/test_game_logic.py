from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# FIX: New tests to verify Bug 1 (inverted hints) is resolved.
# Generated with Claude Code to confirm that the hint messages now
# match the correct direction.

def test_too_high_hint_says_go_lower():
    # When guess is too high, the message must tell the player to go LOWER
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    # When guess is too low, the message must tell the player to go HIGHER
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


# Challenge 1: Advanced Edge-Case Testing
# These tests expose inputs that parse_guess currently accepts without
# validating against the game's actual range (1 to max).
# Identified with Copilot — each case reveals a gap in input handling.

def test_negative_number_is_parsed_but_out_of_range():
    # Edge case: "-5" is a valid integer but below the game's minimum of 1.
    # parse_guess currently accepts it — this test documents that behaviour
    # and flags it as something that should eventually be range-validated.
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5  # accepted, but -5 is below game range

def test_decimal_is_truncated_not_rounded():
    # Edge case: "3.9" gets converted to int via truncation, becoming 3 not 4.
    # A player typing 3.9 expecting it to round to 4 would get the wrong result.
    ok, value, err = parse_guess("3.9")
    assert ok is True
    assert value == 3  # truncated, not rounded

def test_extremely_large_number_is_accepted():
    # Edge case: a huge number like 999999 is way outside any difficulty range
    # but parse_guess accepts it with no upper bound check.
    ok, value, err = parse_guess("999999")
    assert ok is True
    assert value == 999999  # no ceiling enforced
