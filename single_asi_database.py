# single_asi_database.py

import os
import sqlite3
import json


def get_db_path():
    # This file is scenario_generator/single_asi_database.py
    current_file = os.path.abspath(__file__)

    # Go up one directory to project root (because scenario_generator/ is one level below root)
    project_root = os.path.dirname(os.path.dirname(current_file))

    # Compose full path to data/asi_scenarios.db
    data_dir = os.path.join(project_root, 'data')

    # Create data directory if missing
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return os.path.join(data_dir, 'asi_scenarios.db')


def init_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scenarios (
            id TEXT PRIMARY KEY,
            title TEXT,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_scenario(scenario):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO scenarios (id, title, data) VALUES (?, ?, ?)",
              (scenario["id"], scenario["title"], json.dumps(scenario)))
    conn.commit()
    conn.close()
