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

I used GitHub Copilot (via VS Code) throughout Phase 2 to help identify the root causes of the bug, to plan the refactor, and generate the tests.

**Correct AI suggestion — fixing the inverted hints:**
Copilot identified that `check_guess` in `app.py` had the hint messages swapped: when `guess > secret` (too high) it returned `"📈 Go HIGHER!"` instead of `"📉 Go LOWER!"`. Copilot suggested swapping the emoji and direction text so `"Too High"` maps to `"Go LOWER!"` and `"Too Low"` maps to `"Go HIGHER!"`. I verified this by running the two new pytest cases `test_too_high_hint_says_go_lower` and `test_too_low_hint_says_go_higher`, in which both passed and then confirmed in the live Streamlit game that guessing too high now correctly told me to go lower.

**Incorrect/misleading AI suggestion — the score on "Too High!":**
At one point Copilot suggested that rewarding +5 points for a "Too High" guess on even attempts inside `update_score` was intentional game design rather than a bug. I accepted this explanation at first but after playing the game I realized it felt unfair and random and getting rewarded for a wrong guess makes no sense to a player. I rejected that explanation and left the scoring logic unchanged for now, noting it as a future fix since it wasn't one of my two targeted bugs for this phase.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed only when two things were both true; the pytest test for that specific bug passed, and I could confirm the correct behavior by playing the game in my browser.

**Test 1 — Inverted hints (pytest):** I added `test_too_high_hint_says_go_lower`, which calls `check_guess(80, 50)` and asserts the returned message contains `"LOWER"`. Before the fix this would have failed because the old code returned `"Go HIGHER!"`. After moving the corrected `check_guess` into `logic_utils.py`, all 5 tests passed with `pytest tests/ -v`.

**Test 2 — New Game button (manual):** I ran the game with `python -m streamlit run app.py`, won a round, and then clicked "New Game." Before the fix the page looped back to "You already won." After adding `st.session_state.status = "playing"` to the new_game handler, the button correctly reset the game and let me play a fresh round.

Copilot also helped me catch that the original tests were checking `result == "Win"` but `check_guess` returns a tuple, whichh means the tests would have always failed even on the correct logic. Copilot suggested unpacking the tuple in each test using `outcome, message = check_guess(...)`, which was the right approach.

---

## 4. What did you learn about Streamlit and state?

In the original app, the secret number appeared to behave differently depending on which attempt you were on, not because the stored number changed, but because on every even numbered attempt the code silently converted it to a string with `secret = str(st.session_state.secret)`. This meant the comparison in `check_guess` flipped between numeric and string logic every other guess, which was making the hints feel random and the target feel like it was moving.

Streamlit works differently from a normal Python script. Every time you click a button or type something Streamlit reruns the entire script from top to bottom. Normally this would reset all your variables to their starting values. Session state is Streamlit's solution. Any value stored in `st.session_state` stays put between interactions so you can track things like the secret number, attempt count, and score without them being wiped on every click.

The fix that gave the game a stable secret was already partly in place. The `if "secret" not in st.session_state:` guard meant the secret was only generated once. The real fix was removing the string conversion entirely and always passing `st.session_state.secret` (the integer) directly to `check_guess`. After that the hints became consistent and trustworthy.

---

## 5. Looking ahead: your developer habits

One developer habit I want to carry forward is writing a test before or immediately after a fix, not after the whole project is done. When I added `test_too_high_hint_says_go_lower` right after fixing `check_guess`, I could instantly confirm the fix was correct. That feedback loop was much tighter than just running the app and guessing and it gave me confidence the fix was real and not just coincidentally working.

Next time I work with AI on a coding task, I would ask it to explain the bug before proposing a fix. In this project, I sometimes accepted a fix without fully understanding why the original code was wrong. Going forward, I'll treat AI suggestions as a starting point to reason through and not a final answer to paste in.

This project changed the way I think about AI-generated code because it showed me that code can look completely correct at a glance, with proper syntax, reasonable variable names, familiar patterns and still contain logic that quietly breaks the product in ways that only show up during real use. AI writes convincing code but not necessarily a correct code and that distinction is now something I'll keep in mind.

---

## Challenge 5: AI Model Comparison

**The bug I tested with:** The inverted hints bug, `check_guess` returned `"Go HIGHER!"` when the guess was too high and `"Go LOWER!"` when it was too low.

**Prompt I used:** *"I have a Python function called `check_guess(guess, secret)`. When the guess is higher than the secret it returns 'Go HIGHER!' and when it's lower it returns 'Go LOWER!'. The hints are backwards and the player can never win by following them. How do I fix this issue?"*

---

**GitHub Copilot (VS Code inline):**
Copilot responded directly in the editor with an inline suggestion that swapped the two return strings. It changed `"Go HIGHER!"` to `"Go LOWER!"` and vice versa without any extra explanation. The suggestion appeared as a ghost text diff and I could accept it with Tab in one keystroke. It was fast and the fix was technically correct, but Copilot did not explain why the original code was wrong, it just handed me the corrected version. If I had not already understood the bug, I would have accepted the fix without really learning anything about it.

**ChatGPT (GPT-4o, chat interface):**
ChatGPT gave a longer response. It started by restating the problem in plain English, *"when `guess > secret` the player needs to go lower, not higher, so the condition and its message are swapped"*, before showing the corrected code. It also suggested adding a comment to the function to make the logic self-documenting. The explanation made it easier to understand the root cause and not just copy the fix. The trade off is that the response took longer to read and required me to copy code manually from the chat window into my editor.

---

**Which gave a more readable fix?**
Copilot's fix was way more readable than ChatGPT in the sense that it appeared right inside my file with no extra steps. I could see exactly what changed. ChatGPT's fix was embedded inside a block of explanation text which made it slightly harder to extract but the surrounding explanation added context that Copilot skipped.

**Which explained the "why" more clearly?**
ChatGPT explained the "why" more clearly than copilot did. It named the condition and the message pointed in opposite directions before showing the corrected code. Copilot gave me the right answer but treated the fix like autocomplete. For this bug, understanding *why* it was wrong matters more than getting it fixed fast, so ChatGPT was more useful for actually learning from the mistake.
