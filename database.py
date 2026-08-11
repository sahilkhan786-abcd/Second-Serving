"""
database.py
Second Serving - SQLite data layer
All DB access for the app lives here.
"""

import sqlite3
from datetime import datetime, timedelta
import random

DB_NAME = "second_serving.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            business_type TEXT,
            location TEXT,
            rating REAL DEFAULT 5.0,
            total_donations INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS recipients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            org_type TEXT,
            location TEXT,
            capacity_meals INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER,
            food_type TEXT NOT NULL,
            quantity TEXT NOT NULL,
            allergens TEXT,
            pickup_start TEXT,
            pickup_end TEXT,
            status TEXT DEFAULT 'Available',   -- Available, Claimed, Picked Up, Expired
            needs_delivery INTEGER DEFAULT 0,
            claimed_by INTEGER,
            created_at TEXT,
            photo_note TEXT,
            safety_checked INTEGER DEFAULT 0,
            FOREIGN KEY (donor_id) REFERENCES donors(id),
            FOREIGN KEY (claimed_by) REFERENCES recipients(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donation_id INTEGER,
            donor_name TEXT,
            recipient_name TEXT,
            food_type TEXT,
            quantity TEXT,
            issued_at TEXT,
            estimated_meals INTEGER
        )
    """)

    conn.commit()
    conn.close()


def seed_demo_data():
    """Populate the DB with realistic demo data (only if empty)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as c FROM donors")
    if cur.fetchone()["c"] > 0:
        conn.close()
        return

    donors = [
        ("Bagels & Co", "Bakery / Cafe", "Jhamsikhel, Lalitpur", 4.8, 12),
        ("Krishna Bakery", "Bakery", "New Road, Kathmandu", 4.5, 30),
        ("Play, Ink and Eat (PIE)", "Restaurant / Cafe", "Pulchowk, Lalitpur", 4.9, 8),
        ("Wellbeing Bakery", "Bakery", "Baneshwor, Kathmandu", 4.6, 5),
    ]
    cur.executemany(
        "INSERT INTO donors (name, business_type, location, rating, total_donations) VALUES (?,?,?,?,?)",
        donors,
    )

    recipients = [
        ("Kathmandu Valley Shelter", "Shelter", "Koteshwor, Kathmandu", 80),
        ("Hope Food Bank", "Food Bank", "Kalanki, Kathmandu", 150),
        ("Sunrise Children's Home", "Orphanage", "Boudha, Kathmandu", 60),
    ]
    cur.executemany(
        "INSERT INTO recipients (name, org_type, location, capacity_meals) VALUES (?,?,?,?)",
        recipients,
    )
    conn.commit()

    now = datetime.now()
    sample_donations = [
        (1, "Assorted bagels & pastries", "25 pieces", "Gluten, Dairy",
         (now).strftime("%Y-%m-%d %H:%M"), (now + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
         "Available", 0, None, now.strftime("%Y-%m-%d %H:%M:%S"), "Fresh, boxed", 1),
        (2, "Bread loaves", "40 pieces", "Gluten",
         (now).strftime("%Y-%m-%d %H:%M"), (now + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
         "Available", 1, None, now.strftime("%Y-%m-%d %H:%M:%S"), "Day-old, still fresh", 1),
        (3, "Sandwiches & pastries", "15 boxes", "Dairy, Nuts",
         (now).strftime("%Y-%m-%d %H:%M"), (now + timedelta(hours=1, minutes=30)).strftime("%Y-%m-%d %H:%M"),
         "Claimed", 0, 1, (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"), "Individually wrapped", 1),
    ]
    cur.executemany("""
        INSERT INTO donations
        (donor_id, food_type, quantity, allergens, pickup_start, pickup_end,
         status, needs_delivery, claimed_by, created_at, photo_note, safety_checked)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, sample_donations)
    conn.commit()
    conn.close()


# ---------- Donor operations ----------

def add_donor(name, business_type, location):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO donors (name, business_type, location) VALUES (?,?,?)",
        (name, business_type, location),
    )
    conn.commit()
    donor_id = cur.lastrowid
    conn.close()
    return donor_id


def get_donors():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM donors ORDER BY name").fetchall()
    conn.close()
    return rows


def create_donation(donor_id, food_type, quantity, allergens, pickup_start,
                     pickup_end, needs_delivery, photo_note, safety_checked):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO donations
        (donor_id, food_type, quantity, allergens, pickup_start, pickup_end,
         status, needs_delivery, created_at, photo_note, safety_checked)
        VALUES (?,?,?,?,?,?, 'Available', ?, ?, ?, ?)
    """, (donor_id, food_type, quantity, allergens, pickup_start, pickup_end,
          int(needs_delivery), datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          photo_note, int(safety_checked)))
    conn.commit()
    cur.execute("UPDATE donors SET total_donations = total_donations + 1 WHERE id = ?", (donor_id,))
    conn.commit()
    conn.close()


# ---------- Recipient operations ----------

def add_recipient(name, org_type, location, capacity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO recipients (name, org_type, location, capacity_meals) VALUES (?,?,?,?)",
        (name, org_type, location, capacity),
    )
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return rid


def get_recipients():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM recipients ORDER BY name").fetchall()
    conn.close()
    return rows


def get_available_donations():
    conn = get_connection()
    rows = conn.execute("""
        SELECT donations.*, donors.name as donor_name, donors.location as donor_location,
               donors.rating as donor_rating
        FROM donations
        JOIN donors ON donations.donor_id = donors.id
        WHERE donations.status = 'Available'
        ORDER BY donations.pickup_end ASC
    """).fetchall()
    conn.close()
    return rows


def claim_donation(donation_id, recipient_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE donations SET status = 'Claimed', claimed_by = ? WHERE id = ?",
        (recipient_id, donation_id),
    )
    conn.commit()

    # generate a trust & safety receipt automatically
    row = cur.execute("""
        SELECT donations.*, donors.name as donor_name FROM donations
        JOIN donors ON donations.donor_id = donors.id WHERE donations.id = ?
    """, (donation_id,)).fetchone()
    recipient = cur.execute("SELECT name FROM recipients WHERE id = ?", (recipient_id,)).fetchone()

    estimated_meals = estimate_meals(row["quantity"])

    cur.execute("""
        INSERT INTO receipts (donation_id, donor_name, recipient_name, food_type,
                               quantity, issued_at, estimated_meals)
        VALUES (?,?,?,?,?,?,?)
    """, (donation_id, row["donor_name"], recipient["name"], row["food_type"],
          row["quantity"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), estimated_meals))
    conn.commit()
    conn.close()


def mark_picked_up(donation_id):
    conn = get_connection()
    conn.execute("UPDATE donations SET status = 'Picked Up' WHERE id = ?", (donation_id,))
    conn.commit()
    conn.close()


def estimate_meals(quantity_str):
    """Very rough heuristic: pull the first number out of the quantity string."""
    digits = "".join(c if c.isdigit() else " " for c in quantity_str).split()
    n = int(digits[0]) if digits else 5
    return max(1, n)


def get_all_donations():
    conn = get_connection()
    rows = conn.execute("""
        SELECT donations.*, donors.name as donor_name,
               (SELECT name FROM recipients WHERE id = donations.claimed_by) as recipient_name
        FROM donations
        JOIN donors ON donations.donor_id = donors.id
        ORDER BY donations.created_at DESC
    """).fetchall()
    conn.close()
    return rows


def get_receipts():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM receipts ORDER BY issued_at DESC").fetchall()
    conn.close()
    return rows


def get_stats():
    conn = get_connection()
    cur = conn.cursor()
    total_donations = cur.execute("SELECT COUNT(*) c FROM donations").fetchone()["c"]
    total_claimed = cur.execute("SELECT COUNT(*) c FROM donations WHERE status != 'Available'").fetchone()["c"]
    total_meals = cur.execute("SELECT COALESCE(SUM(estimated_meals),0) m FROM receipts").fetchone()["m"]
    active_donors = cur.execute("SELECT COUNT(*) c FROM donors").fetchone()["c"]
    active_recipients = cur.execute("SELECT COUNT(*) c FROM recipients").fetchone()["c"]
    conn.close()
    return {
        "total_donations": total_donations,
        "total_claimed": total_claimed,
        "total_meals": total_meals,
        "active_donors": active_donors,
        "active_recipients": active_recipients,
    }
