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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
