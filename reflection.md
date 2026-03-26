# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

Before designing anything, I thought about what a real pet owner would actually do with this app. I came up with three core actions:

1. **Add a pet** — The owner enters a pet's name and species so the system knows who the tasks are for.
2. **Schedule a task** — The owner adds a care task (like "morning walk" or "medication") with a time, duration, and priority so it can be tracked and planned.
3. **View today's schedule** — The app collects all tasks for the day and displays them in a clear, organized way so the owner knows what to do and when.

These three actions drive the entire design. Everything else in the system exists to support them.

**a. Initial design**

I started with four classes: `Task`, `Pet`, `Owner`, and `Scheduler`.

`Task` is the core data unit — it represents one care activity like a walk or a feeding. It stores what the task is, when it happens, how long it takes, its priority, and whether it's been done.

`Pet` is a simple data container. It just holds a pet's name and species. I kept it simple on purpose because the pet itself doesn't need any behavior — it just needs to be identifiable.

`Owner` is the central manager. It holds the list of pets and the list of tasks. If you want to know anything about what's scheduled, you go through the owner.

`Scheduler` is the system's brain. It takes an `Owner` as input and provides methods for organizing tasks — sorting by time, filtering by pet or status, and detecting conflicts. I separated it from `Owner` so that the scheduling logic is isolated and easier to test on its own.

**b. Design changes**

My first instinct was to give each `Pet` its own list of tasks, so tasks would live under the pet they belonged to. But I stopped and thought about it more carefully — the owner is the one actually doing the tasks, not the pet. Walking the dog, giving medication, feeding — these are all things the owner does. So it made more sense to have `Owner` hold the tasks list, and just give each `Task` a `pet_name` field to say which pet it's for.

This also makes the `Pet` class simpler. A pet just needs a name and species. The `Owner` manages everything else. The `Scheduler` can then pull all tasks from the owner in one place, without having to loop through each pet's individual list.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three main constraints: time (tasks have a scheduled HH:MM time), priority (low, medium, or high), and frequency (once, daily, or weekly). I decided that time was the most important constraint to sort by because a daily schedule only makes sense if tasks appear in the order they actually happen. Priority is visible in the table so the owner can make judgment calls, but the scheduler doesn't reorder tasks by priority — time wins. This felt right because a medication at 09:00 needs to happen at 09:00 regardless of whether it's labeled "high" or "medium."

**b. Tradeoffs**

One tradeoff I made is that conflict detection only flags tasks with the exact same time — it doesn't check for overlapping durations. For example, if "Morning walk" starts at 08:00 and takes 30 minutes, and "Feeding" starts at 08:15, those tasks technically overlap but my system won't flag them.

I made this choice intentionally because handling duration overlap would add a lot of complexity — you'd have to convert HH:MM strings into minutes, calculate end times, and compare ranges instead of single values. For a first version of the app, exact-time conflicts are already useful and easy to understand. The tradeoff is that the scheduler might miss some real scheduling issues, but it also stays simple and predictable, which matters more at this stage.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the project in a few different ways. Early on, it helped me think through the class design — I described the scenario and asked it to help me brainstorm attributes and methods for each class. That was probably the most useful part because it gave me a starting point I could react to rather than starting from a blank page. Later I used it more for implementation help, like figuring out how to handle recurring tasks with `timedelta` and how to structure the conflict detection logic. The prompts that worked best were specific ones — asking "what should go in the Scheduler vs the Owner" got a much more useful response than just asking "help me design this app."

**b. Judgment and verification**

The AI's first design suggestion put the task list inside each `Pet`, so every pet would own its own tasks. That felt off to me — the owner is the one doing the tasks, not the pet. I pushed back on it and we redesigned so the `Owner` holds all tasks and each `Task` has a `pet_name` field to say which animal it's for. I verified this was the right call by thinking through a concrete scenario: if I want to see all tasks for today, it's much simpler to just loop through `owner.tasks` than to loop through every pet and collect their individual lists. The cleaner retrieval logic confirmed the redesign was worth it.

---

## 4. Testing and Verification

**a. What you tested**

I tested seven behaviors: marking a task complete, adding tasks to the owner, sorting tasks chronologically, daily recurrence creating a next-day task, conflict detection flagging duplicate times, filtering returning an empty list for a pet with no tasks, and confirming that same-time tasks for *different* pets are not flagged as conflicts. These tests mattered because they cover both the happy paths (things working normally) and edge cases (empty results, no false positives) that could silently break the app.

**b. Confidence**

I'm confident the core scheduling logic works correctly — all 7 tests pass and the behaviors feel solid. The main thing I'd test next with more time is duration-based overlap detection. Right now the system only catches exact same-time conflicts, so two tasks that overlap (like 08:00 for 30 min and 08:15 for 20 min) would slip through. That's a known limitation I'd address in the next version.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the class design. Keeping `Owner` as the central manager and `Scheduler` as a separate reasoning layer made the code easy to follow and test independently. The `Scheduler` doesn't store any data — it just reads from the `Owner` and processes it. That separation made it easy to add sorting, filtering, and conflict detection without touching the data model at all.

**b. What you would improve**

If I had another iteration, I'd add duration-aware conflict detection so the app catches overlapping tasks, not just exact same-time ones. I'd also add a date picker to the UI so you could view schedules for future days, not just today. Right now recurring tasks get created but you can't easily see them until that date arrives.

**c. Key takeaway**

The biggest thing I learned is that using AI well means staying in the driver's seat. It's easy to just accept whatever the AI suggests, but the best results came when I had an opinion and pushed back. The task-ownership redesign is a good example — the AI gave me a reasonable first answer, but it wasn't the right one for my use case. Treating AI like a collaborator you can argue with, rather than an authority you just follow, made the final design much better.
