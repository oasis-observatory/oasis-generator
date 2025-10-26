# multi_asi_scenario.py

import argparse
import sqlite3
import uuid
import json
import os
from datetime import datetime, timezone

from multi_asi_ollama_client import generate_multi_asi_narrative
from multi_asi_database import save_multi_asi_scenario


def get_db_path():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "data", "asi_scenarios.db")


def fetch_asi_scenarios(num_asis=5):
    db_path = get_db_path()
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, data FROM scenarios ORDER BY RANDOM() LIMIT ?", (num_asis,))
    rows = cursor.fetchall()

    if not rows:
        raise ValueError("No ASI scenarios found in the database.")

    asis = []
    for idx, row in enumerate(rows):
        scenario_id, title, scenario_json = row

        try:
            scenario_data = json.loads(scenario_json)
        except json.JSONDecodeError:
            print(f"⚠️ Skipping malformed JSON for scenario ID: {scenario_id}")
            continue

        asi_id = f"asi-{idx + 1}"
        core = {
            "origin": scenario_data.get("origin", {}),
            "architecture": scenario_data.get("architecture", {}),
            "oversight_structure": scenario_data.get("impact_and_control", {}).get("oversight_structure", "unknown"),
            "agency_level": scenario_data.get("core_capabilities", {}).get("agency_level"),
            "autonomy_degree": scenario_data.get("core_capabilities", {}).get("autonomy_degree"),
            "alignment_score": scenario_data.get("core_capabilities", {}).get("alignment_score"),
            "goal": scenario_data.get("goals_and_behavior", {}).get("stated_goal"),
        }

        asis.append({
            "id": asi_id,
            "scenario_id": scenario_id,
            "title": title,
            "core_parameters": core
        })

    conn.close()

    if len(asis) < num_asis:
        print(f"⚠️ Only {len(asis)} scenarios were available.")

    return asis


def create_multi_asi_scenario(num_asis=5):
    asis = fetch_asi_scenarios(num_asis=num_asis)
    overall_title = " vs ".join(asi["title"] for asi in asis)
    narrative = generate_multi_asi_narrative(overall_title, asis)

    scenario_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    scenario = {
        "id": scenario_id,
        "title": overall_title,
        "metadata": {
            "created": timestamp,
            "last_updated": timestamp,
            "version": 1,
            "source": "composed"
        },
        "asis": asis,
        "scenario_content": {
            "title": overall_title,
            "narrative": narrative,
            "timeline": {
                "phase_1": {
                    "years": "1970–2100",
                    "description": "Interaction phase between ASIs"
                }
            }
        },
        "observations": {
            "cooperation_level": "uncertain",
            "conflict_potential": "moderate",
            "intervention_requirements": "TBD"
        }
    }

    save_multi_asi_scenario(scenario)
    print(f"✅ Multi-ASI scenario '{overall_title}' saved.")


def main():
    parser = argparse.ArgumentParser(description="Generate multi-ASI speculative scenario.")
    parser.add_argument(
        '-n', '--num-asis',
        type=int,
        default=5,
        help='Number of ASI scenarios to combine (default: 5)'
    )

    args = parser.parse_args()
    create_multi_asi_scenario(num_asis=args.num_asis)


if __name__ == "__main__":
    main()
