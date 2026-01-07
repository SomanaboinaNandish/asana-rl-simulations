-- =========================================================
-- Reset schema (idempotent & safe re-runs)
-- =========================================================

PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS task_tags;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS sections;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS team_memberships;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS organizations;

PRAGMA foreign_keys = ON;

-- =========================================================
-- ORGANIZATIONS
-- =========================================================

CREATE TABLE organizations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

-- =========================================================
-- USERS
-- =========================================================

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,               -- IC, Manager, Director, Exec
    created_at TIMESTAMP NOT NULL,
    last_active_at TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE INDEX idx_users_org_id ON users(org_id);

-- =========================================================
-- TEAMS
-- =========================================================

CREATE TABLE teams (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE INDEX idx_teams_org_id ON teams(org_id);

-- =========================================================
-- TEAM MEMBERSHIPS (Many-to-Many)
-- =========================================================

CREATE TABLE team_memberships (
    user_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    joined_at TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id, team_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

CREATE INDEX idx_team_memberships_team_id ON team_memberships(team_id);

-- =========================================================
-- PROJECTS
-- =========================================================

CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    name TEXT NOT NULL,
    project_type TEXT NOT NULL,        -- sprint, bugfix, infra, campaign, roadmap, support
    created_at TIMESTAMP NOT NULL,
    archived BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

CREATE INDEX idx_projects_team_id ON projects(team_id);

-- =========================================================
-- SECTIONS (Kanban Columns)
-- =========================================================

CREATE TABLE sections (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,                -- Backlog, In Progress, Done, etc.
    position INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE INDEX idx_sections_project_id ON sections(project_id);

-- =========================================================
-- TASKS (Tasks + Subtasks via parent_task_id)
-- =========================================================

CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT,
    parent_task_id TEXT,               -- NULL for top-level tasks
    name TEXT NOT NULL,
    description TEXT,
    assignee_id TEXT,
    status TEXT NOT NULL,               -- not_started, in_progress, completed
    due_date DATE,
    created_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (section_id) REFERENCES sections(id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(id),
    FOREIGN KEY (assignee_id) REFERENCES users(id)
);

CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_section_id ON tasks(section_id);
CREATE INDEX idx_tasks_assignee_id ON tasks(assignee_id);
CREATE INDEX idx_tasks_parent_task_id ON tasks(parent_task_id);

-- =========================================================
-- COMMENTS
-- =========================================================

CREATE TABLE comments (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    author_id TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id),
    FOREIGN KEY (author_id) REFERENCES users(id)
);

CREATE INDEX idx_comments_task_id ON comments(task_id);
CREATE INDEX idx_comments_author_id ON comments(author_id);

-- =========================================================
-- TAGS
-- =========================================================

CREATE TABLE tags (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- =========================================================
-- TASK ↔ TAG ASSOCIATION
-- =========================================================

CREATE TABLE task_tags (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

CREATE INDEX idx_task_tags_tag_id ON task_tags(tag_id);
