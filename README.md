# Asana RL Simulation – Enterprise Seed Data Generator

This repository contains a fully reproducible pipeline for generating **realistic, enterprise-scale seed data** for a simulated Asana environment.  
The dataset is designed to support **reinforcement learning (RL) environments** for computer-use AI agents operating on project management workflows.

---

## 📌 Overview

The simulation represents a **B2B SaaS company** with approximately **6,000 employees**, spanning Engineering, Product, Marketing, Sales, and Operations teams.  
It captures realistic organizational structure, project workflows, task hierarchies, due dates, and collaboration patterns.

The focus is on **data realism**, **temporal consistency**, and **relational integrity**, avoiding synthetic shortcuts such as uniform task names or evenly distributed deadlines.

---

## 🧱 Key Entities Modeled

- Organizations
- Users (ICs, Managers, Directors, Executives)
- Teams & Team Memberships
- Projects
- Sections (Kanban columns)
- Tasks & Subtasks (hierarchical)
- Comments (task discussions)

---

## 📊 Data Characteristics

- ~6,000 users
- ~80 teams
- ~700–800 projects
- ~60,000+ tasks (including subtasks)
- ~120,000+ comments
- Realistic due-date distributions
- Unassigned tasks, overdue tasks, archived projects included intentionally

---

## 📁 Repository Structure

asana-rl-simulations/
├── schema.sql # SQLite schema (idempotent)
├── src/
│ ├── main.py # Orchestrates full data generation
│ ├── generators/ # Entity-specific generators
│ │ ├── users.py
│ │ ├── teams.py
│ │ ├── team_memberships.py
│ │ ├── projects.py
│ │ ├── sections.py
│ │ ├── tasks.py
│ │ └── comments.py
│ └── utils/
│ └── db.py # Database initialization logic
├── data/
│ ├── Indian-Male-Names.csv
│ └── Indian-Female-Names.csv
└── output/
└── asana_simulation.sqlite # Generated database (ignored in git)

How to Run

### Requirements
- Python 3.10+
- SQLite (bundled with Python)

### Run the generator

From the project root:

```bash
py src/main.py
Documentation

Full methodology, schema explanation, and ER diagram are provided in the Google Doc submitted alongside this repository as part of the take-home assignment.



---

## ✅ What To Do Now

1️⃣ Create a new file in your repo root called **`README.md`**  
2️⃣ Paste the content above  
3️⃣ Save the file  

Then run:

```bash
git add README.md
git commit -m "Add README with project overview and usage"
git push

contact : nandish.s22@iiits.in
