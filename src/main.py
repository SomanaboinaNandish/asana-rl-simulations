from utils.db import init_db
from generators.users import generate_users
from generators.teams import generate_teams
from generators.team_memberships import generate_team_memberships
from generators.projects import generate_projects
from generators.sections import generate_sections
from generators.tasks import generate_tasks
from generators.comments import generate_comments


import uuid
from datetime import datetime


def create_org(conn):
    org_id = str(uuid.uuid4())
    conn.execute(
        """
        INSERT INTO organizations (id, name, created_at)
        VALUES (?, ?, ?)
        """,
        (org_id, "Acme SaaS Inc.", datetime.utcnow())
    )
    conn.commit()
    return org_id


def main():
    conn = init_db()
    org_id = create_org(conn)

    generate_users(conn, org_id)
    generate_teams(conn, org_id)
    generate_team_memberships(conn)

    generate_projects(conn, org_id)
    generate_sections(conn)
    generate_tasks(conn)
    generate_comments(conn)



if __name__ == "__main__":
    main()
