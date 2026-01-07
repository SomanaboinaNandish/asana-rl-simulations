import uuid
import random
from datetime import datetime, timedelta


COMMENT_TEMPLATES = [
    "Can you take a look at this?",
    "This is blocked due to a dependency.",
    "I’ve pushed an update for this.",
    "Let’s discuss this in the next sync.",
    "This should be ready for review.",
    "Any updates on this?",
    "Looks good to me.",
    "We might need clarification here.",
    "Following up on this task.",
    "Resolved as discussed."
]


def generate_comments(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, assignee_id, created_at, completed_at
        FROM tasks
    """)
    tasks = cursor.fetchall()

    cursor.execute("SELECT id FROM users")
    user_ids = [u[0] for u in cursor.fetchall()]

    comments = []

    for task_id, assignee_id, created_at_str, completed_at_str in tasks:
        # Convert SQLite timestamps to datetime
        created_at = datetime.fromisoformat(created_at_str)

        completed_at = (
            datetime.fromisoformat(completed_at_str)
            if completed_at_str
            else None
        )

        # 0–6 comments per task (weighted)
        comment_count = random.choices(
            [0, 1, 2, 3, 4, 5, 6],
            weights=[25, 20, 20, 15, 10, 7, 3]
        )[0]

        if comment_count == 0:
            continue

        possible_authors = list(user_ids)
        if assignee_id:
            possible_authors.append(assignee_id)

        latest_time = completed_at or datetime.utcnow()

        max_days = max(1, (latest_time - created_at).days)

        for _ in range(comment_count):
            comment_time = created_at + timedelta(
                days=random.randint(0, max_days)
            )

            comments.append((
                str(uuid.uuid4()),
                task_id,
                random.choice(possible_authors),
                random.choice(COMMENT_TEMPLATES),
                comment_time
            ))

    cursor.executemany(
        """
        INSERT INTO comments
        (id, task_id, author_id, body, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        comments
    )

    conn.commit()
    print(f"Inserted {len(comments)} comments")
