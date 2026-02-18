# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The game launched and appeared functional at first glance. There was a text input, a submit button, and a sidebar with difficulty settings. But once I started playing, things quickly went wrong.

**Bug 1: The hints were backwards (Easy mode)**
- **Expected:** If my guess was lower than the secret number, the game should tell me to go higher.
- **What actually happened:** On Easy mode, I started guessing at 8 and kept following the "Go LOWER" hints all the way down toward 0. When I ran out of attempts, the game revealed the secret was 83 — a number far above where the hints were pointing me. The hints were completely inverted: "Go LOWER!" appeared when I needed to go higher. Following the hints made it impossible to ever win.

**Bug 2: The "New Game" button did nothing after winning (Hard mode)**
- **Expected:** After winning a round, clicking "New Game" should reset the game so I can play again.
- **What actually happened:** On Hard mode I won a round, but when I clicked "New Game" the page refreshed and immediately showed "You already won. Start a new game to play again." again — stuck in a loop. The button appeared to respond but the game never actually reset. The code resets the attempts and secret number but never resets the game `status` back to `"playing"`, so the game stops again instantly on every rerun.

**Bug 3: "Hard" difficulty was actually easier than "Normal"**
- **Expected:** "Hard" mode should be harder — meaning a bigger range of numbers to guess from, making it less likely to guess correctly.
- **What actually happened:** The Hard difficulty uses a range of 1–50, while Normal uses 1–100. Hard was literally half the range of Normal, which is the opposite of what "Hard" should mean. A player choosing Hard for a challenge would actually find it easier to guess correctly by chance.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

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
