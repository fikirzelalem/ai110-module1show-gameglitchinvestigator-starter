# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I ran the game it launched and appeared functional at first glance. There was a text input, a submit button, and a sidebar with difficulty settings and an option to get a hint. But once I started playing, things quickly started going wrong.

**Bug 1: The hints were backwards (Normal mode)**
- **Expected:** If my guess was lower than the secret number, the game should tell me to go higher.
- **What actually happened:** On Normal mode, I started guessing at 8 and kept following the "Go LOWER" hints all the way down toward 0. When I ran out of attempts, the game revealed the secret number was 83, a number far above where the hints were pointing me. The hints were completely inverted and "Go LOWER!" appeared when I needed to go higher. For this reason, following the hints made it impossible to ever win the game.

**Bug 2:"Hard" difficulty was actually easier than "Normal" difficulty**
- **Expected:** "Hard" mode should be harder than both Easy mode and Normal mode meaning there is a bigger range of numbers to guess from, making it less likely to guess correctly.
- **What actually happened:** The Hard difficulty uses a range of 1–50, while Normal uses 1–100. Hard was literally half the range of Normal, which is the opposite of what "Hard" should mean. A player choosing Hard for the challenge would actually find it easier to guess correctly by chance.

**Bug 3: The "New Game" button did nothing after winning (Hard mode)**
- **Expected:** After winning a round on Hard mode on the first try, clicking the "New Game" button should reset the game so I can play it again.
- **What actually happened:** On Hard mode I won a round, but when I clicked "New Game" the page refreshed and immediately showed "You already won. Start a new game to play again." again and it got stuck in a loop. The button appeared to respond but the game never actually reset. The code resets the attempts and secret number but never resets the game `status` back to `"playing"`, so the game stops again instantly on every re-run.

---

## 2. How did you use AI as a teammate?

I used GitHub Copilot (via VS Code) throughout Phase 2 to help identify root causes, plan the refactor, and generate tests.

**Correct AI suggestion — fixing the inverted hints:**
Copilot identified that `check_guess` in `app.py` had the hint messages swapped: when `guess > secret` (too high), it returned `"📈 Go HIGHER!"` instead of `"📉 Go LOWER!"`. Copilot suggested swapping the emoji and direction text so `"Too High"` maps to `"Go LOWER!"` and `"Too Low"` maps to `"Go HIGHER!"`. I verified this by running the two new pytest cases `test_too_high_hint_says_go_lower` and `test_too_low_hint_says_go_higher` — both passed — and then confirmed in the live Streamlit game that guessing too high now correctly told me to go lower.

**Incorrect/misleading AI suggestion — the score on "Too High":**
At one point Copilot suggested that rewarding +5 points for a "Too High" guess on even attempts inside `update_score` was intentional game design rather than a bug. I accepted this explanation at first, but after playing the game I realized it felt unfair and random — getting rewarded for a wrong guess makes no sense to a player. I rejected that explanation and left the scoring logic unchanged for now, noting it as a future fix since it wasn't one of my two targeted bugs for this phase.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed only when two things were both true: the pytest test for that specific bug passed, and I could confirm the correct behavior by playing the live game in my browser.

**Test 1 — Inverted hints (pytest):** I added `test_too_high_hint_says_go_lower`, which calls `check_guess(80, 50)` and asserts the returned message contains `"LOWER"`. Before the fix this would have failed because the old code returned `"Go HIGHER!"`. After moving the corrected `check_guess` into `logic_utils.py`, all 5 tests passed with `pytest tests/ -v`.

**Test 2 — New Game button (manual):** I ran the game with `python -m streamlit run app.py`, won a round, then clicked "New Game." Before the fix the page looped back to "You already won." After adding `st.session_state.status = "playing"` to the new_game handler, the button correctly reset the game and let me play a fresh round.

Copilot also helped me catch that the original tests were checking `result == "Win"` but `check_guess` returns a tuple, meaning the tests would have always failed even on correct logic. Copilot suggested unpacking the tuple in each test using `outcome, message = check_guess(...)`, which was the right approach.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
