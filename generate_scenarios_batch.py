# generate_scenarios_batch.py

from single_asi_scenario import generate_scenario
import sqlite3
import json

def fetch_latest_scenarios(limit):
    conn = sqlite3.connect("../data/asi_scenarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, data FROM scenarios ORDER BY ROWID DESC LIMIT ?", (limit,))
    results = cursor.fetchall()
    conn.close()

    return [json.loads(row[1]) for row in results]

def main():
    try:
        num = int(input("🔢 How many single-ASI scenarios do you want to generate? "))
    except ValueError:
        print("❌ Please enter a valid number.")
        return

    print(f"🚀 Generating {num} scenario(s)...\n")
    for i in range(num):
        print(f"🧠 Generating scenario {i + 1}...")
        generate_scenario()

    print("\n✅ Done! Fetching the latest generated scenarios...\n")
    scenarios = fetch_latest_scenarios(num)

    for idx, scenario in enumerate(reversed(scenarios), 1):
        print(f"--- Scenario {idx} ---")
        print(f"🆔 ID: {scenario['id']}")
        print(f"📛 Title: {scenario['title']}")
        print(f"🌱 Origin: {scenario['origin']}")
        print(f"🏗 Architecture: {scenario['architecture']}")
        print(f"🧠 Oversight: {scenario['impact_and_control']['oversight_structure']}")
        print(f"🎯 Goal: {scenario['goals_and_behavior']['stated_goal']}")
        print(f"📄 Narrative (preview): {scenario['scenario_content']['narrative'][:150]}...\n")

if __name__ == "__main__":
    main()
