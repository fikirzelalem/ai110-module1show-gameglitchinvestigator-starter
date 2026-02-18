def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive numeric range for a given difficulty level.

    Maps a difficulty string to a (low, high) tuple that defines the range
    of possible secret numbers for that difficulty. Higher difficulties use
    a wider range to make the game harder.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        A tuple (low, high) where both values are inclusive integers.
        Defaults to (1, 100) if an unrecognised difficulty is passed.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 500)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse a raw string input from the player into an integer guess.

    Accepts whole numbers and decimal strings (decimals are truncated, not
    rounded). Returns a three-element tuple so callers can distinguish a
    valid guess from an error without relying on exceptions.

    Note:
        This function does not validate the guess against the game's range.
        A value like -5 or 999999 will be returned as valid. Range checking
        is the responsibility of the caller.

    Args:
        raw: The raw string typed by the player. May be None or empty.

    Returns:
        A tuple of (ok, guess_int, error_message) where:
            - ok (bool): True if the input was successfully parsed.
            - guess_int (int | None): The parsed integer, or None on failure.
            - error_message (str | None): A human-readable error string if
              parsing failed, otherwise None.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("3.9")
        (True, 3, None)
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare a player's guess to the secret number and return a result.

    Determines whether the guess is correct, too high, or too low, and
    returns both a machine-readable outcome label and a human-readable
    hint message for display in the UI.

    Args:
        guess: The integer the player guessed.
        secret: The secret integer the player is trying to find.

    Returns:
        A tuple of (outcome, message) where:
            - outcome (str): One of "Win", "Too High", or "Too Low".
            - message (str): A player-facing hint string with emoji.

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(80, 50)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(20, 50)
        ('Too Low', '📈 Go HIGHER!')
    """
    # FIX: Bug 1 — corrected inverted hint messages. When guess > secret the
    # player needs to go lower, and when guess < secret they need to go higher.
    # Refactored from app.py using Copilot Agent mode.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate and return the updated score after a guess.

    Applies a scoring formula based on the outcome of the guess and which
    attempt number it was. Winning earlier yields more points. Wrong guesses
    generally deduct points, though the current formula has an asymmetry on
    even-numbered attempts for "Too High" outcomes (a known quirk).

    Args:
        current_score: The player's score before this guess.
        outcome: The result of the guess — one of "Win", "Too High", or
            "Too Low". Any other value leaves the score unchanged.
        attempt_number: The 1-based attempt count for this guess. Used to
            calculate diminishing win points and the "Too High" quirk.

    Returns:
        The updated integer score after applying the scoring rules.

    Examples:
        >>> update_score(0, "Win", 1)
        80
        >>> update_score(100, "Too Low", 3)
        95
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
