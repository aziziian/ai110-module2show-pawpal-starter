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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
