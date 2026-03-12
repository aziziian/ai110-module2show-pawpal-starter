"""
PawPal+ system classes.
Owner holds all pets and tasks. Tasks reference a pet by name.
"""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    """A single pet care activity assigned to a specific pet."""
    description: str
    pet_name: str
    time: str                        # "HH:MM" format, e.g. "08:00"
    duration: int                    # minutes
    priority: str                    # "low", "medium", "high"
    frequency: str = "once"          # "once", "daily", "weekly"
    completed: bool = False
    due_date: Optional[date] = None

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task done and return a new recurring task if applicable."""
        self.completed = True
        if self.frequency == "daily" and self.due_date:
            return Task(
                description=self.description,
                pet_name=self.pet_name,
                time=self.time,
                duration=self.duration,
                priority=self.priority,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(days=1),
            )
        if self.frequency == "weekly" and self.due_date:
            return Task(
                description=self.description,
                pet_name=self.pet_name,
                time=self.time,
                duration=self.duration,
                priority=self.priority,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(weeks=1),
            )
        return None


@dataclass
class Pet:
    """A pet belonging to an owner."""
    name: str
    species: str                     # "dog", "cat", "other"


class Owner:
    """Manages a collection of pets and their care tasks."""

    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def add_task(self, task: Task) -> None:
        """Add a care task to the owner's task list."""
        self.tasks.append(task)

    def get_tasks_for_pet(self, pet_name: str) -> list[Task]:
        """Return all tasks that belong to a specific pet."""
        return [t for t in self.tasks if t.pet_name == pet_name]

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all pets."""
        return self.tasks


class Scheduler:
    """Organizes and analyzes tasks for an owner."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_todays_tasks(self, today: date) -> list[Task]:
        """Return tasks whose due_date matches today, or all tasks if no due_date is set."""
        tasks = self.owner.get_all_tasks()
        result = []
        for task in tasks:
            if task.due_date is None or task.due_date == today:
                result.append(task)
        return result

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks chronologically by their time field (HH:MM)."""
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(
        self,
        tasks: list[Task],
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> list[Task]:
        """Filter tasks by pet name and/or completion status."""
        result = tasks
        if pet_name is not None:
            result = [t for t in result if t.pet_name == pet_name]
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        return result

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return warning messages for any two tasks with the same pet and same time."""
        warnings = []
        seen = {}
        for task in tasks:
            key = (task.pet_name, task.time)
            if key in seen:
                warnings.append(
                    f"Conflict: '{task.description}' and '{seen[key]}' "
                    f"are both scheduled for {task.pet_name} at {task.time}"
                )
            else:
                seen[key] = task.description
        return warnings
