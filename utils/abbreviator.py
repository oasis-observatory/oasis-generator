# utils/abbreviator.py

import os
import sqlite3

def get_db_path():
    # Get absolute path to project root (assumes 'scenario_generator/utils' folder structure)
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))  # up 3 dirs
    data_dir = os.path.join(project_root, 'data')

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return os.path.join(data_dir, 'asi_scenarios.db')

def get_next_scenario_number(db_path=None):
    """Returns the next scenario number as an integer based on row count in the DB."""
    if db_path is None:
        db_path = get_db_path()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM scenarios")
    count = cursor.fetchone()[0]
    conn.close()
    return count + 1

def short_code(value):
    """Generate a short code (up to 3 letters) from a string."""
    parts = value.split('-') if isinstance(value, str) else []
    if parts:
        # Take first letter of each part, max 3 letters
        code = ''.join(p[0].upper() for p in parts)[:3]
    else:
        # If no dashes, just take first 3 letters uppercase
        code = value[:3].upper() if isinstance(value, str) else "UNK"
    return code

def generate_title_abbreviation(core):
    """
    Generates a scenario abbreviation code from the core parameters dictionary.
    Format: IO-DD-ARC-TOPO-OVS-OEFF-SUB-NNN
    where:
        IO = initial_origin (e.g., Corporate => C)
        DD = development_dynamics (Engineered => E)
        ARC = architecture (Monolithic => M)
        TOPO = deployment_topology (Centralized => C)
        OVS = oversight_type (Corporate => C)
        OEFF = oversight_effectiveness (Strong => S)
        SUB = substrate (Neuromorphic => N)
        NNN = scenario number, zero-padded
    """
    abbrev_parts = [
        short_code(core.get("initial_origin", "UNK")),
        short_code(core.get("development_dynamics", "UNK")),
        short_code(core.get("architecture", "UNK")),
        short_code(core.get("deployment_topology", "UNK")),
        short_code(core.get("oversight_type", "UNK")),
        short_code(core.get("oversight_effectiveness", "UNK")),
        short_code(core.get("substrate", "UNK"))
    ]

    scenario_number = get_next_scenario_number()
    abbrev = '-'.join(abbrev_parts)
    return f"{abbrev}-{scenario_number:03d}"
