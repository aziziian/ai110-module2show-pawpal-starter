"""
PawPal+ demo script.
Creates an owner, two pets, and several tasks, then prints today's schedule.
"""

from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

TODAY = date.today()


def print_schedule(tasks: list[Task]) -> None:
    """Print a list of tasks in a readable format."""
    if not tasks:
        print("  (no tasks)")
        return
    for task in tasks:
        status = "✓" if task.completed else "○"
        print(
            f"  [{status}] {task.time}  {task.description}"
            f"  ({task.pet_name}, {task.duration} min, {task.priority} priority)"
        )


def main():
    # --- Set up owner and pets ---
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="dog")
    bella = Pet(name="Bella", species="cat")

    owner.add_pet(mochi)
    owner.add_pet(bella)

    # --- Add tasks (intentionally out of time order) ---
    owner.add_task(Task(
        description="Evening walk",
        pet_name="Mochi",
        time="18:00",
        duration=30,
        priority="high",
        frequency="daily",
        due_date=TODAY,
    ))
    owner.add_task(Task(
        description="Morning walk",
        pet_name="Mochi",
        time="08:00",
        duration=20,
        priority="high",
        frequency="daily",
        due_date=TODAY,
    ))
    owner.add_task(Task(
        description="Medication",
        pet_name="Bella",
        time="09:00",
        duration=5,
        priority="high",
        frequency="daily",
        due_date=TODAY,
    ))
    owner.add_task(Task(
        description="Midday feeding",
        pet_name="Mochi",
        time="12:00",
        duration=10,
        priority="medium",
        frequency="daily",
        due_date=TODAY,
    ))
    owner.add_task(Task(
        description="Grooming",
        pet_name="Bella",
        time="15:00",
        duration=20,
        priority="low",
        frequency="weekly",
        due_date=TODAY,
    ))

    # --- Build schedule ---
    scheduler = Scheduler(owner)
    todays_tasks = scheduler.get_todays_tasks(TODAY)
    sorted_tasks = scheduler.sort_tasks(todays_tasks)

    # --- Print full schedule ---
    print("=" * 50)
    print(f"  PawPal+ Daily Schedule — {TODAY}")
    print(f"  Owner: {owner.name}")
    print("=" * 50)
    print_schedule(sorted_tasks)

    # --- Filter: Mochi only ---
    print("\n--- Mochi's tasks ---")
    mochi_tasks = scheduler.filter_tasks(sorted_tasks, pet_name="Mochi")
    print_schedule(mochi_tasks)

    # --- Conflict detection ---
    print("\n--- Conflict check ---")
    conflicts = scheduler.detect_conflicts(sorted_tasks)
    if conflicts:
        for warning in conflicts:
            print(f"  ⚠ {warning}")
    else:
        print("  No conflicts found.")

    # --- Demo: mark a task complete and show recurrence ---
    print("\n--- Marking 'Morning walk' complete ---")
    morning_walk = sorted_tasks[0]  # first task after sorting is 08:00
    next_task = morning_walk.mark_complete()
    if next_task:
        owner.add_task(next_task)
        print(f"  '{morning_walk.description}' marked done.")
        print(f"  Next recurrence created: {next_task.description} on {next_task.due_date}")

    print("=" * 50)


if __name__ == "__main__":
    main()
