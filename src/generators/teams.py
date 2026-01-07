import uuid
import random
from datetime import datetime

TEAM_CATEGORIES = {
    "Engineering": [
        "Payments Platform",
        "Core Backend",
        "Frontend Experience",
        "DevOps & Infrastructure",
        "Data Platform",
        "Security Engineering"
    ],
    "Product": [
        "Product Strategy",
        "User Experience",
        "Growth Product"
    ],
    "Marketing": [
        "Growth Marketing",
        "Brand Marketing",
        "Content Marketing"
    ],
    "Sales": [
        "Enterprise Sales",
        "SMB Sales",
        "Sales Operations"
    ],
    "Operations": [
        "Customer Support",
        "Business Operations",
        "IT Operations"
    ]
}

TEAM_DISTRIBUTION = {
    "Engineering": 0.45,
    "Product": 0.15,
    "Marketing": 0.15,
    "Sales": 0.10,
    "Operations": 0.15
}


def generate_teams(conn, org_id, total_teams=80):
    teams = []
    now = datetime.utcnow()

    for category, weight in TEAM_DISTRIBUTION.items():
        count = int(total_teams * weight)
        names = TEAM_CATEGORIES[category]

        for i in range(count):
            team_id = str(uuid.uuid4())
            team_name = random.choice(names)

            teams.append((
                team_id,
                org_id,
                f"{team_name} {i+1}",
                now
            ))

    conn.executemany(
        """
        INSERT INTO teams (id, org_id, name, created_at)
        VALUES (?, ?, ?, ?)
        """,
        teams
    )

    conn.commit()
    print(f"Inserted {len(teams)} teams")

    return [t[0] for t in teams]
