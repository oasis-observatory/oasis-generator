# single_asi_database.py – OASIS Observatory v3.0: 10-COLUMN HYBRID SCHEMA
import sqlite3
import json
from typing import Dict, Any, List
from typing import Optional
from pathlib import Path
from jsonschema import validate
from common.schema_loader import load_schema

DB_PATH = Path("../data/asi_scenarios.db")
SCHEMA = load_schema("asi_scenario_schema.json")


def init_db() -> sqlite3.Connection:
    """Initialize DB with 10-column schema and indexes."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 10-COLUMN HYBRID SCHEMA
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scenarios (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        initial_origin TEXT,
        agency_level REAL,
        alignment_score REAL,
        autonomy_degree TEXT,
        deployment_strategy TEXT,
        impact_domains TEXT,  -- JSON array as text
        created_at TEXT,
        scenario_json TEXT NOT NULL
    )
    """)

    # CRITICAL INDEXES (for 80% of queries)
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_title ON scenarios(title)",
        "CREATE INDEX IF NOT EXISTS idx_origin ON scenarios(initial_origin)",
        "CREATE INDEX IF NOT EXISTS idx_agency ON scenarios(agency_level)",
        "CREATE INDEX IF NOT EXISTS idx_alignment ON scenarios(alignment_score)",
        "CREATE INDEX IF NOT EXISTS idx_autonomy ON scenarios(autonomy_degree)",
        "CREATE INDEX IF NOT EXISTS idx_strategy ON scenarios(deployment_strategy)",
        "CREATE INDEX IF NOT EXISTS idx_domains ON scenarios(impact_domains)",
        "CREATE INDEX IF NOT EXISTS idx_created ON scenarios(created_at)"
    ]
    for idx in indexes:
        cursor.execute(idx)

    conn.commit()
    return conn


def save_scenario(scenario: Dict[str, Any]) -> bool:
    """Validate + save with 10 extracted fields."""
    try:
        validate(instance=scenario, schema=SCHEMA)
    except Exception as e:
        print(f"[VALIDATION ERROR] {e}")
        return False

    conn = init_db()
    cursor = conn.cursor()

    # Extract fields
    origin = scenario["origin"]["initial_origin"]
    core = scenario["core_capabilities"]
    impact = scenario["impact_and_control"]
    created = scenario["metadata"]["created"]

    cursor.execute("""
    INSERT OR REPLACE INTO scenarios 
    (id, title, initial_origin, agency_level, alignment_score,
     autonomy_degree, deployment_strategy, impact_domains,
     created_at, scenario_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        scenario["id"],
        scenario["title"],
        origin,
        core["agency_level"],
        core["alignment_score"],
        core["autonomy_degree"],
        impact["deployment_strategy"],
        json.dumps(impact["impact_domains"]),  # Store as JSON string
        created,
        json.dumps(scenario)
    ))

    conn.commit()
    conn.close()
    return True


def query_scenarios(
    filters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    if filters is None:
        filters = {}


    """POWER QUERY: Filter by any of the 10 columns."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    where = []
    params = []

    # Map filters to columns
    mapping = {
        "min_agency": ("agency_level >= ?", "agency_level"),
        "max_agency": ("agency_level <= ?", "agency_level"),
        "min_alignment": ("alignment_score >= ?", "alignment_score"),
        "origin": ("initial_origin = ?", "initial_origin"),
        "autonomy": ("autonomy_degree = ?", "autonomy_degree"),
        "strategy": ("deployment_strategy = ?", "deployment_strategy"),
        "domain": ("impact_domains LIKE ?", "impact_domains"),
        "after": ("created_at > ?", "created_at"),
        "before": ("created_at < ?", "created_at"),
    }

    for key, value in filters.items():
        if key not in mapping:
            continue
        col_clause, _ = mapping[key]
        where.append(col_clause)
        if key == "domain":
            params.append(f"%{value}%")
        else:
            params.append(value)

    where_sql = " AND ".join(where) if where else "1=1"
    order_by = filters.get("order_by", "agency_level DESC")

    cursor.execute(f"""
    SELECT scenario_json FROM scenarios 
    WHERE {where_sql} 
    ORDER BY {order_by}
    """, params)

    results = [json.loads(row[0]) for row in cursor.fetchall()]
    conn.close()
    return results


# === EXAMPLE USAGE ===
if __name__ == "__main__":
    # High-risk rogue systems from 2025
    high_risk = query_scenarios({
        "min_agency": 0.8,
        "origin": "rogue",
        "after": "2025-01-01T00:00:00+00:00",
        "order_by": "alignment_score ASC"
    })
    print(f"Found {len(high_risk)} high-risk scenarios")
