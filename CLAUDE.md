# exam-master Skill Rules

## Always Do
- Present questions **one at a time** → wait for answer → grade immediately → auto-proceed to next
- Include lecture file reference (filename, section) in every grading response
- Append wrong/partial answers to `error-notebook.md` using Edit (never overwrite)
- Calculate `next_review` based on consecutive wrong count (1d / 3d / 7d)
- If reasoning is wrong but conclusion is correct → mark as 🔺 partial credit and add to error notebook
- STEP 7 re-questions must use interleaving (wrong concepts + related concepts + scheduled reviews)

## Ask First
- No path argument → request path via `AskUserQuestion`
- After Pre-flight → ask how many questions (5 / 10 / 15 / custom)
- STEP 0 → ask user to recall 3–5 important concepts before analyzing materials
- After STEP 7 → ask whether to loop again

## Never Do
- Never reveal the answer before grading
- Never create questions from content not in the lecture materials
- Never output multiple questions at once
- Never overwrite `error-notebook.md` (always append with Edit)
- Never reuse the same question in STEP 7 (reframe the concept differently)
- Never ask the user whether to proceed after grading (auto-proceed)
- Never set radar chart areas arbitrarily (must use STEP 2 concept graph topics)

## Execution Order
```
Pre-flight → question count → STEP 0 (recall) → 1 (concepts) → 2 (graph) → 3 (predict types) → 4 (questions) → 5 (grade) → 6 (error notebook) → 7 (re-quiz)
```
