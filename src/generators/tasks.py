import uuid
import random
from datetime import datetime, timedelta
import math


STATUS_BY_SECTION = {
    "Backlog": "not_started",
    "To Do": "not_started",
    "Planned": "not_started",
    "Ideas": "not_started",
    "Reported": "not_started",

    "In Progress": "in_progress",
    "Fixing": "in_progress",
    "Implementing": "in_progress",
    "Writing": "in_progress",
    "Investigating": "in_progress",

    "Code Review": "in_progress",
    "Testing": "in_progress",
    "Review": "in_progress",

    "Done": "completed",
    "Resolved": "completed",
    "Released": "completed",
    "Launched": "completed",
    "Published": "completed",
    "Closed": "completed"
}


def sample_due_date(created_at):
    """
    Realistic distribution:
    - 10% no due date
    - 25% within 7 days
    - 40% within 30 days
    - 20% within 90 days
    - 5% overdue
    """
    r = random.random()

    if r < 0.10:
        return None
    elif r < 0.35:
        return created_at + timedelta(days=random.randint(1, 7))
    elif r < 0.75:
        return created_at + timedelta(days=random.randint(8, 30))
    elif r < 0.95:
        return created_at + timedelta(days=random.randint(31, 90))
    else:
        return created_at - timedelta(days=random.randint(1, 14))


def lognormal_task_count(mean=40):
    """Skewed, realistic task count per project"""
    return max(5, int(random.lognormvariate(math.log(mean), 0.6)))


def generate_tasks(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.id, p.project_type, p.created_at, s.id, s.name
        FROM projects p
        JOIN sections s ON p.id = s.project_id
    """)
    rows = cursor.fetchall()

    cursor.execute("SELECT id FROM users")
    user_ids = [r[0] for r in cursor.fetchall()]

    tasks = []
    now = datetime.utcnow()

    # Group sections by project
    project_sections = {}
    for project_id, project_type, created_at_str, section_id, section_name in rows:
        project_sections.setdefault(project_id, {
            "project_type": project_type,
            "created_at": datetime.fromisoformat(created_at_str),
            "sections": []
        })
        project_sections[project_id]["sections"].append((section_id, section_name))

    for project_id, data in project_sections.items():
        project_created_at = data["created_at"]
        task_count = lognormal_task_count()

        for _ in range(task_count):
            section_id, section_name = random.choice(data["sections"])
            status = STATUS_BY_SECTION.get(section_name, "not_started")

            created_at = project_created_at + timedelta(
                days=random.randint(0, 60)
            )

            due_date = sample_due_date(created_at)

            completed_at = None
            if status == "completed":
                completed_at = created_at + timedelta(days=random.randint(1, 14))
                completed_at = min(completed_at, now)

            assignee_id = random.choice(user_ids) if random.random() > 0.15 else None

            task_id = str(uuid.uuid4())

            tasks.append((
                task_id,
                project_id,
                section_id,
                None,
                f"Task – {task_id[:6]}",
                "Auto-generated task with realistic lifecycle.",
                assignee_id,
                status,
                due_date,
                created_at,
                completed_at
            ))

            # -------- SUBTASKS (30%) --------
            if random.random() < 0.30:
                subtask_count = random.randint(1, 4)

                for i in range(subtask_count):
                    sub_created = created_at + timedelta(days=random.randint(0, 3))
                    sub_completed = None

                    if status == "completed":
                        sub_completed = sub_created + timedelta(
                            days=random.randint(1, 7)
                        )

                    tasks.append((
                        str(uuid.uuid4()),
                        project_id,
                        section_id,
                        task_id,
                        f"Subtask {i + 1}",
                        "Generated subtask.",
                        assignee_id,
                        status,
                        due_date,
                        sub_created,
                        sub_completed
                    ))

    cursor.executemany(
        """
        INSERT INTO tasks
        (id, project_id, section_id, parent_task_id, name, description,
         assignee_id, status, due_date, created_at, completed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        tasks
    )

    conn.commit()
    print(f"Inserted {len(tasks)} tasks (including subtasks)")
