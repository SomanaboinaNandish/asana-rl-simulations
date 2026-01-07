import uuid
import random
from datetime import datetime, timedelta

PROJECT_TYPES = {
    "Engineering": ["sprint", "bugfix", "infra"],
    "Product": ["roadmap", "discovery"],
    "Marketing": ["campaign", "content"],
    "Sales": ["pipeline", "outreach"],
    "Operations": ["support", "ops"]
}

PROJECT_NAME_TEMPLATES = {
    "sprint": [
        "Sprint {n} – Core Improvements",
        "Sprint {n} – Feature Delivery"
    ],
    "bugfix": [
        "Bug Bash – Q{q}",
        "Stability Improvements"
    ],
    "infra": [
        "Infrastructure Upgrade",
        "Platform Reliability"
    ],
    "roadmap": [
        "Product Roadmap – H{h}",
        "Feature Planning"
    ],
    "discovery": [
        "User Research Initiative",
        "Discovery Sprint"
    ],
    "campaign": [
        "Marketing Campaign – Q{q}",
        "Product Launch Campaign"
    ],
    "content": [
        "Content Calendar – Q{q}",
        "SEO Content Plan"
    ],
    "pipeline": [
        "Sales Pipeline Review",
        "Lead Follow-up Campaign"
    ],
    "outreach": [
        "Outbound Outreach – Q{q}",
        "Customer Acquisition"
    ],
    "support": [
        "Customer Support Queue",
        "Escalations Handling"
    ],
    "ops": [
        "Operational Improvements",
        "Process Optimization"
    ]
}


def generate_projects(conn, org_id, projects_per_team=(6, 12)):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM teams")
    teams = cursor.fetchall()

    projects = []
    now = datetime.utcnow()

    for team_id, team_name in teams:
        category = team_name.split()[0]  # Engineering, Product, etc.
        possible_types = PROJECT_TYPES.get(category, ["ops"])

        project_count = random.randint(*projects_per_team)

        for i in range(project_count):
            project_type = random.choice(possible_types)
            template = random.choice(PROJECT_NAME_TEMPLATES[project_type])

            project_name = template.format(
                n=random.randint(1, 50),
                q=random.randint(1, 4),
                h=random.randint(1, 2)
            )

            created_at = now - timedelta(days=random.randint(30, 180))
            archived = random.random() < 0.15  # 15% archived

            projects.append((
                str(uuid.uuid4()),
                team_id,
                project_name,
                project_type,
                created_at,
                archived
            ))

    cursor.executemany(
        """
        INSERT INTO projects
        (id, team_id, name, project_type, created_at, archived)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        projects
    )

    conn.commit()
    print(f"Inserted {len(projects)} projects")

    return [p[0] for p in projects]
