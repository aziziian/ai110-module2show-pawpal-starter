# PawPal+ 🐾

**PawPal+** is a smart pet care scheduling app built with Python and Streamlit. It helps a busy pet owner stay on top of daily care tasks for multiple pets — with automatic sorting, filtering, conflict detection, and recurring task support.

---

## Features

- Add multiple pets with name and species
- Schedule care tasks with time, duration, priority, and frequency
- View today's tasks sorted chronologically in a clean table
- Mark tasks complete directly from the browser
- Recurring tasks (daily/weekly) auto-generate the next occurrence when marked done
- Filter tasks by pet or completion status
- Conflict warnings when two tasks are booked for the same pet at the same time

---

## Smarter Scheduling

PawPal+ goes beyond a simple task list. The `Scheduler` class provides four smart features:

- **Sorting** — tasks are always displayed in chronological order by time, so the owner sees their day in sequence
- **Filtering** — the UI lets you filter tasks by pet name or completion status to focus on what matters right now
- **Conflict warnings** — if two tasks are scheduled for the same pet at the same time, the app shows a warning so the owner can fix it before the day starts
- **Recurring tasks** — marking a daily or weekly task complete automatically creates the next occurrence, so the owner never has to re-enter routine care tasks

---

## Testing PawPal+

To run the test suite:

```bash
python -m pytest
```

The tests cover 7 behaviors:

| Test | What it verifies |
|---|---|
| Task completion | `mark_complete()` flips status to done |
| Task count | `add_task()` correctly grows the owner's task list |
| Sorting | Tasks come back in chronological time order |
| Daily recurrence | Completing a daily task creates one for the next day |
| Conflict detection | Same pet + same time triggers a warning |
| Empty pet filter | Filtering a pet with no tasks returns `[]`, not an error |
| No false conflicts | Same time for different pets is not flagged |

**Confidence: ★★★★☆**
The core behaviors are all covered and all 7 tests pass. The one area not tested is the Streamlit UI layer itself, since that requires a browser — but all the logic behind the UI is verified here.

---

## Demo

Add your screenshot below after taking one with `streamlit run app.py`:

<a href="/course_images/ai110/your_screenshot_name.png" target="_blank"><img src='/course_images/ai110/your_screenshot_name.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

---

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Run the CLI demo

```bash
python main.py
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
