"""
Basic tests for PawPal+ core classes.
Run with: python -m pytest
"""

from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler


# --- Test 1: mark_complete() changes a task's status ---
def test_task_mark_complete():
    """A task should be marked done after calling mark_complete()."""
    task = Task(
        description="Morning walk",
        pet_name="Mochi",
        time="08:00",
        duration=20,
        priority="high",
        frequency="once",
        due_date=date.today(),
    )
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


# --- Test 2: adding a task to Owner increases the task count ---
def test_owner_add_task_increases_count():
    """Owner's task list should grow by 1 each time add_task() is called."""
    owner = Owner(name="Jordan")
    assert len(owner.tasks) == 0

    owner.add_task(Task(
        description="Feeding",
        pet_name="Bella",
        time="07:00",
        duration=10,
        priority="high",
    ))
    assert len(owner.tasks) == 1

    owner.add_task(Task(
        description="Medication",
        pet_name="Bella",
        time="09:00",
        duration=5,
        priority="high",
    ))
    assert len(owner.tasks) == 2
