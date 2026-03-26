"""
Automated test suite for PawPal+ core classes.
Run with: python -m pytest
"""

from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_task(description="Walk", pet_name="Mochi", time="08:00",
              frequency="once", due_date=None):
    """Helper to create a Task with sensible defaults."""
    return Task(
        description=description,
        pet_name=pet_name,
        time=time,
        duration=20,
        priority="high",
        frequency=frequency,
        due_date=due_date or date.today(),
    )


def make_owner_with_tasks(*tasks):
    """Helper to create an Owner with a set of tasks already added."""
    owner = Owner(name="Jordan")
    owner.add_pet(Pet(name="Mochi", species="dog"))
    owner.add_pet(Pet(name="Bella", species="cat"))
    for task in tasks:
        owner.add_task(task)
    return owner


# ── Test 1: mark_complete() changes status ────────────────────────────────────
def test_task_mark_complete():
    """A task should be marked done after calling mark_complete()."""
    task = make_task()
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


# ── Test 2: adding a task increases count ─────────────────────────────────────
def test_owner_add_task_increases_count():
    """Owner's task list should grow by 1 each time add_task() is called."""
    owner = Owner(name="Jordan")
    assert len(owner.tasks) == 0
    owner.add_task(make_task(description="Walk"))
    assert len(owner.tasks) == 1
    owner.add_task(make_task(description="Feeding", time="07:00"))
    assert len(owner.tasks) == 2


# ── Test 3: tasks sort in chronological order ─────────────────────────────────
def test_sort_tasks_chronological():
    """Scheduler.sort_tasks() should return tasks ordered earliest to latest."""
    t1 = make_task(description="Evening walk", time="18:00")
    t2 = make_task(description="Morning walk", time="08:00")
    t3 = make_task(description="Medication", time="09:00")

    owner = make_owner_with_tasks(t1, t2, t3)
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_tasks(owner.get_all_tasks())

    times = [t.time for t in sorted_tasks]
    assert times == ["08:00", "09:00", "18:00"]


# ── Test 4: daily recurring task creates next-day task ────────────────────────
def test_daily_recurrence_creates_next_task():
    """Marking a daily task complete should return a new task due the next day."""
    today = date.today()
    task = make_task(frequency="daily", due_date=today)

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False
    assert next_task.description == task.description


# ── Test 5: conflict detection flags same pet + same time ─────────────────────
def test_conflict_detection_same_pet_same_time():
    """Scheduler should return a warning when two tasks share a pet and time."""
    t1 = make_task(description="Walk", pet_name="Mochi", time="08:00")
    t2 = make_task(description="Feeding", pet_name="Mochi", time="08:00")

    owner = make_owner_with_tasks(t1, t2)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    assert len(conflicts) == 1
    assert "Mochi" in conflicts[0]
    assert "08:00" in conflicts[0]


# ── Test 6: pet with no tasks returns empty filter ────────────────────────────
def test_filter_pet_with_no_tasks():
    """Filtering by a pet that has no tasks should return an empty list."""
    task = make_task(pet_name="Mochi")
    owner = make_owner_with_tasks(task)
    scheduler = Scheduler(owner)

    bella_tasks = scheduler.filter_tasks(owner.get_all_tasks(), pet_name="Bella")
    assert bella_tasks == []


# ── Test 7: no conflict when same time but different pets ─────────────────────
def test_no_conflict_different_pets_same_time():
    """Two tasks at the same time for different pets should NOT be flagged."""
    t1 = make_task(description="Walk", pet_name="Mochi", time="08:00")
    t2 = make_task(description="Feeding", pet_name="Bella", time="08:00")

    owner = make_owner_with_tasks(t1, t2)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    assert conflicts == []
