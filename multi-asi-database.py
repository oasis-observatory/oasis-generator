# multi-asi-database.py

import sqlite3
import json
import os

db_path = "../data/multi_asi_scenarios.db"

def init_multi_asi_db():
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS multi_asi_scenarios (
                id TEXT PRIMARY KEY,
                title TEXT,
                metadata TEXT,
                asis TEXT,
                scenario_content TEXT,
                observations TEXT
            )
        """)
        conn.commit()
        conn.close()

def save_multi_asi_scenario(scenario):
    init_multi_asi_db()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO multi_asi_scenarios (
            id, title, metadata, asis, scenario_content, observations
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        scenario["id"],
        scenario["title"],
        json.dumps(scenario.get("metadata", {})),
        json.dumps(scenario.get("asis", [])),
        json.dumps(scenario.get("scenario_content", {})),
        json.dumps(scenario.get("observations", {}))
    ))

    conn.commit()
    conn.close()
