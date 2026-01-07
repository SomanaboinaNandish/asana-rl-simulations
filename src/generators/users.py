import uuid
import random
import csv
from datetime import datetime, timedelta
from pathlib import Path

# Resolve project root
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

MALE_NAMES_FILE = DATA_DIR / "Indian-Male-Names.csv"
FEMALE_NAMES_FILE = DATA_DIR / "Indian-Female-Names.csv"

ROLES = [
    ("IC", 0.75),
    ("Manager", 0.15),
    ("Director", 0.08),
    ("Exec", 0.02)
]

def weighted_choice(choices):
    r = random.random()
    upto = 0
    for value, weight in choices:
        if upto + weight >= r:
            return value
        upto += weight
    return choices[-1][0]


def load_names(csv_path):
    names = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                name = row[0].strip()
                if name.lower() != "name":  # skip header if present
                    names.append(name)
    return names


def generate_users(conn, org_id, n_users=6000):
    male_names = load_names(MALE_NAMES_FILE)
    female_names = load_names(FEMALE_NAMES_FILE)

    assert male_names and female_names, "Name CSVs cannot be empty"

    users = []
    used_emails = set()

    base_date = datetime.utcnow() - timedelta(days=365 * 4)

    for i in range(n_users):
        gender = random.choice(["male", "female"])

        if gender == "male":
            first_name = random.choice(male_names)
        else:
            first_name = random.choice(female_names)

        # Simple last-name generation (realistic for Indian context)
        last_name = random.choice(male_names + female_names)

        full_name = f"{first_name} {last_name}"

        # Email collision handling
        email_base = f"{first_name}.{last_name}".lower()
        email = f"{email_base}@acme.com"
        suffix = 1
        while email in used_emails:
            suffix += 1
            email = f"{email_base}{suffix}@acme.com"

        used_emails.add(email)

        user_id = str(uuid.uuid4())
        created_at = base_date + timedelta(days=random.randint(0, 1200))
        last_active_at = created_at + timedelta(days=random.randint(1, 900))

        users.append((
            user_id,
            org_id,
            full_name,
            email,
            weighted_choice(ROLES),
            created_at,
            last_active_at
        ))

    conn.executemany(
        """
        INSERT INTO users
        (id, org_id, full_name, email, role, created_at, last_active_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        users
    )

    conn.commit()
    print(f"Inserted {len(users)} users")
