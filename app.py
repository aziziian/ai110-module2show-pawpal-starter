import streamlit as st
from datetime import date

from pawpal_system import Task, Pet, Owner, Scheduler

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A smart pet care scheduler for busy owners.")

# ── Session state: create Owner once and reuse it ────────────────────────────
# st.session_state acts like a memory box — it survives every time the page reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")

owner: Owner = st.session_state.owner

# ── Section 1: Owner setup ────────────────────────────────────────────────────
st.subheader("1. Owner")
owner_name = st.text_input("Your name", value=owner.name or "Jordan")
owner.name = owner_name

# ── Section 2: Add a pet ──────────────────────────────────────────────────────
st.subheader("2. Add a Pet")

col1, col2 = st.columns(2)
with col1:
    pet_name_input = st.text_input("Pet name", value="Mochi")
with col2:
    species_input = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    # Check we don't add duplicates
    existing_names = [p.name for p in owner.pets]
    if pet_name_input.strip() == "":
        st.warning("Please enter a pet name.")
    elif pet_name_input in existing_names:
        st.warning(f"{pet_name_input} is already added.")
    else:
        owner.add_pet(Pet(name=pet_name_input, species=species_input))
        st.success(f"Added {pet_name_input} the {species_input}!")

# Show current pets
if owner.pets:
    st.write("**Your pets:**", ", ".join(p.name for p in owner.pets))
else:
    st.info("No pets added yet.")

# ── Section 3: Schedule a task ────────────────────────────────────────────────
st.subheader("3. Schedule a Task")

if not owner.pets:
    st.info("Add at least one pet above before scheduling tasks.")
else:
    pet_names = [p.name for p in owner.pets]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_desc = st.text_input("Task description", value="Morning walk")
        task_pet = st.selectbox("For which pet?", pet_names)
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
        task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add Task"):
        if task_desc.strip() == "":
            st.warning("Please enter a task description.")
        else:
            new_task = Task(
                description=task_desc,
                pet_name=task_pet,
                time=task_time,
                duration=task_duration,
                priority=task_priority,
                frequency=task_frequency,
                due_date=date.today(),
            )
            owner.add_task(new_task)
            st.success(f"Task '{task_desc}' added for {task_pet} at {task_time}.")

st.divider()

# ── Section 4: Today's Schedule ───────────────────────────────────────────────
st.subheader("4. Today's Schedule")

scheduler = Scheduler(owner)
todays_tasks = scheduler.get_todays_tasks(date.today())
sorted_tasks = scheduler.sort_tasks(todays_tasks)

# Conflict warnings
conflicts = scheduler.detect_conflicts(sorted_tasks)
if conflicts:
    st.error("**Scheduling conflicts detected** — two tasks are booked at the same time for the same pet. Please adjust the times below.")
    for warning in conflicts:
        st.warning(f"⚠ {warning}")
elif sorted_tasks:
    st.success("No scheduling conflicts — your day looks good!")

if not sorted_tasks:
    st.info("No tasks scheduled for today. Add some above!")
else:
    # Build a display-friendly list of dicts for st.table
    table_data = []
    for task in sorted_tasks:
        table_data.append({
            "Time": task.time,
            "Pet": task.pet_name,
            "Task": task.description,
            "Duration": f"{task.duration} min",
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Done": "✓" if task.completed else "○",
        })
    st.table(table_data)

    # Mark complete buttons
    st.write("**Mark a task complete:**")
    incomplete = [t for t in sorted_tasks if not t.completed]
    if not incomplete:
        st.success("All tasks for today are done!")
    else:
        for i, task in enumerate(incomplete):
            label = f"Complete: {task.time} — {task.description} ({task.pet_name})"
            if st.button(label, key=f"complete_{i}"):
                next_task = task.mark_complete()
                if next_task:
                    owner.add_task(next_task)
                    st.success(f"Done! Next '{task.description}' scheduled for {next_task.due_date}.")
                else:
                    st.success(f"'{task.description}' marked complete.")
                st.rerun()

# ── Section 5: Filter tasks ───────────────────────────────────────────────────
if sorted_tasks and owner.pets:
    st.subheader("5. Filter Tasks")

    filter_pet = st.selectbox(
        "Show tasks for pet",
        ["All pets"] + [p.name for p in owner.pets],
        key="filter_pet",
    )
    filter_done = st.selectbox(
        "Show",
        ["All", "Incomplete only", "Completed only"],
        key="filter_done",
    )

    filtered = sorted_tasks
    if filter_pet != "All pets":
        filtered = scheduler.filter_tasks(filtered, pet_name=filter_pet)
    if filter_done == "Incomplete only":
        filtered = scheduler.filter_tasks(filtered, completed=False)
    elif filter_done == "Completed only":
        filtered = scheduler.filter_tasks(filtered, completed=True)

    if filtered:
        filter_table = []
        for task in filtered:
            filter_table.append({
                "Time": task.time,
                "Pet": task.pet_name,
                "Task": task.description,
                "Priority": task.priority,
                "Done": "✓" if task.completed else "○",
            })
        st.table(filter_table)
    else:
        st.info("No tasks match this filter.")
