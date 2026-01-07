import random
from datetime import datetime


def generate_team_memberships(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT id, role FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT id FROM teams")
    teams = [row[0] for row in cursor.fetchall()]

    memberships = []
    now = datetime.utcnow()

    for user_id, role in users:
        # Managers & Execs belong to more teams
        if role == "IC":
            team_count = random.choice([1, 1, 2])
        elif role == "Manager":
            team_count = random.choice([2, 3])
        else:
            team_count = random.choice([3, 4])

        assigned_teams = random.sample(teams, team_count)

        for team_id in assigned_teams:
            memberships.append((
                user_id,
                team_id,
                now
            ))

    cursor.executemany(
        """
        INSERT OR IGNORE INTO team_memberships (user_id, team_id, joined_at)
        VALUES (?, ?, ?)
        """,
        memberships
    )

    conn.commit()
    print(f"Inserted {len(memberships)} team memberships")
