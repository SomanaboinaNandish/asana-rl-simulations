import uuid

SECTION_TEMPLATES = {
    "sprint": ["Backlog", "In Progress", "Code Review", "Done"],
    "bugfix": ["Reported", "Fixing", "Testing", "Resolved"],
    "infra": ["Planned", "Implementing", "Monitoring", "Completed"],
    "roadmap": ["Ideas", "Planned", "In Progress", "Released"],
    "discovery": ["Research", "Synthesis", "Decisions"],
    "campaign": ["Ideas", "Draft", "Review", "Launched"],
    "content": ["Planned", "Writing", "Editing", "Published"],
    "pipeline": ["Leads", "Contacted", "Negotiation", "Closed"],
    "outreach": ["Targets", "Contacted", "Responses"],
    "support": ["New", "Investigating", "Waiting", "Closed"],
    "ops": ["To Do", "In Progress", "Done"]
}


def generate_sections(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, project_type FROM projects")
    projects = cursor.fetchall()

    sections = []

    for project_id, project_type in projects:
        names = SECTION_TEMPLATES.get(project_type, ["To Do", "In Progress", "Done"])

        for position, name in enumerate(names):
            sections.append((
                str(uuid.uuid4()),
                project_id,
                name,
                position
            ))

    cursor.executemany(
        """
        INSERT INTO sections
        (id, project_id, name, position)
        VALUES (?, ?, ?, ?)
        """,
        sections
    )

    conn.commit()
    print(f"Inserted {len(sections)} sections")
