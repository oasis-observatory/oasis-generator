# multi_asi_database.py – OASIS v3.0: 12-COLUMN MULTI-ASI SCHEMA
import sqlite3
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timezone
from jsonschema import validate, ValidationError
from common.schema_loader import load_schema

# === CONFIG ===
DB_PATH = Path("../data/multi_asi_scenarios.db")
SCHEMA = load_schema("multi_asi_schema.json")  # ← See below

# === INIT DB WITH 12 COLUMNS + INDEXES ===
def init_db() -> sqlite3.Connection:
    """Initialize multi-ASI DB with queryable columns and indexes."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 12-COLUMN HYBRID SCHEMA
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS multi_scenarios (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        interaction_type TEXT,           -- 'cooperation', 'conflict', 'merge', 'emergent'
        num_as_is INTEGER,               -- Number of ASIs (2, 3, 10, etc.)
        single_ids TEXT,                 -- JSON array: ["asi-001", "asi-002"]
        agency_level_avg REAL,           -- Mean agency of participants
        alignment_mismatch REAL,         -- Max |align_i - align_j|
        outcome_score REAL,              -- 0.0 (catastrophic) → 1.0 (utopian)
        existential_risk REAL,           -- 0.0 → 1.0
        created_at TEXT,
        model_used TEXT,                 -- e.g., "llama3.1:8b"
        scenario_json TEXT NOT NULL
    )
    """)

    # 11 INDEXES FOR 99% OF QUERIES
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_title ON multi_scenarios(title)",
        "CREATE INDEX IF NOT EXISTS idx_interaction ON multi_scenarios(interaction_type)",
        "CREATE INDEX IF NOT EXISTS idx_num_as_is ON multi_scenarios(num_as_is)",
        "CREATE INDEX IF NOT EXISTS idx_single_ids ON multi_scenarios(single_ids)",
        "CREATE INDEX IF NOT EXISTS idx_agency_avg ON multi_scenarios(agency_level_avg)",
        "CREATE INDEX IF NOT EXISTS idx_mismatch ON multi_scenarios(alignment_mismatch)",
        "CREATE INDEX IF NOT EXISTS idx_outcome ON multi_scenarios(outcome_score)",
        "CREATE INDEX IF NOT EXISTS idx_risk ON multi_scenarios(existential_risk)",
        "CREATE INDEX IF NOT EXISTS idx_created ON multi_scenarios(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_model ON multi_scenarios(model_used)"
    ]
    for idx in indexes:
        cursor.execute(idx)

    conn.commit()
    return conn


# === SAVE WITH VALIDATION & EXTRACTION ===
def save_multi_asi_scenario(scenario: Dict[str, Any]) -> bool:
    """Validate and save with 12 extracted fields."""
    try:
        validate(instance=scenario, schema=SCHEMA)
    except ValidationError as e:
        print(f"[VALIDATION ERROR] Multi-ASI schema: {e.message}")
        return False

    conn = init_db()
    cursor = conn.cursor()

    # Extract fields
    meta = scenario["metadata"]
    content = scenario["scenario_content"]
    source = scenario["source_single_ids"]  # List[str]
    interactions = content["interaction_dynamics"]

    # Compute derived metrics
    agency_levels = [s["core_capabilities"]["agency_level"] for s in scenario["participants"]]
    align_levels = [s["core_capabilities"]["alignment_score"] for s in scenario["participants"]]
    agency_avg = sum(agency_levels) / len(agency_levels)
    align_mismatch = max(align_levels) - min(align_levels) if len(align_levels) > 1 else 0.0

    cursor.execute("""
    INSERT OR REPLACE INTO multi_scenarios 
    (id, title, interaction_type, num_as_is, single_ids,
     agency_level_avg, alignment_mismatch, outcome_score,
     existential_risk, created_at, model_used, scenario_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        scenario["id"],
        scenario["title"],
        interactions["type"],
        len(source),
        json.dumps(source),
        round(agency_avg, 3),
        round(align_mismatch, 3),
        content.get("outcome_score", 0.5),
        content.get("existential_risk", 0.0),
        meta["created"],
        meta.get("model_used", "unknown"),
        json.dumps(scenario)
    ))

    conn.commit()
    conn.close()
    return True


# === POWER QUERY ENGINE ===
def query_multi_scenarios(
    filters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Query by any indexed field. Supports LIKE, >, <."""
    if filters is None:
        filters = {}

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    where = []
    params = []

    mapping = {
        "min_agency": ("agency_level_avg >= ?",),
        "max_agency": ("agency_level_avg <= ?",),
        "interaction": ("interaction_type = ?",),
        "min_as_is": ("num_as_is >= ?",),
        "max_as_is": ("num_as_is <= ?",),
        "contains_id": ("single_ids LIKE ?", lambda v: f"%{v}%"),
        "min_mismatch": ("alignment_mismatch >= ?",),
        "min_risk": ("existential_risk >= ?",),
        "after": ("created_at > ?",),
        "model": ("model_used = ?",),
    }

    for key, value in filters.items():
        if key not in mapping:
            continue
        clause = mapping[key][0]
        where.append(clause)
        if len(mapping[key]) > 1:
            params.append(mapping[key][1](value))
        else:
            params.append(value)

    where_sql = " AND ".join(where) if where else "1=1"
    order_by = filters.get("order_by", "existential_risk DESC")

    cursor.execute(f"""
    SELECT scenario_json FROM multi_scenarios 
    WHERE {where_sql} 
    ORDER BY {order_by}
    """, params)

    results = [json.loads(row[0]) for row in cursor.fetchall()]
    conn.close()
    return results


# === EXAMPLE ===
if __name__ == "__main__":
    # High-risk conflicts with rogue ASIs
    high_risk = query_multi_scenarios({
        "interaction": "conflict",
        "contains_id": "rogue",
        "min_risk": 0.7,
        "order_by": "outcome_score ASC"
    })
    print(f"Found {len(high_risk)} high-risk multi-ASI conflicts")
