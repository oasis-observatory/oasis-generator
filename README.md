# Open Artificial Superintelligence Scenario Generator v0.1 / OASIS Generator v0.1
Experimental generator producing single-ASI and multi-ASI foresight scenarios using open hermeneutic models.

The **OASIS Generator** is an open-source module for creating narrative simulations of Artificial Superintelligence (ASI) emergence and interaction.
It generates structured scenarios, validates them via schema, and stores them in a local SQLite database for later mapping or analysis. 
It is an experimental tool for producing foresight-style reports on potential futures of Artificial Superintelligence.
It can generate both **single-agent (ASI)** and **multi-agent (poly-ASI)** scenarios, each accompanied by interpretive narratives and thematic indicators.

This module represents the first step toward the larger OASIS Observatory ecosystem.

**Status:** Alpha — open for testing and conceptual feedback.

✳️ Focus: narrative coherence, scenario diversity, and epistemic transparency.
---

## ✨ Features

- Generate **single-ASI** or **multi-ASI** scenario narratives
- Validate results using **JSON Schema**
- Plug in your preferred LLM backend (Ollama, OpenRouter, Claude, etc.)
- Store and query scenarios using **SQLite3**
- Extensible: connect to precursor data or visualization tools
---

## 📦 Installation

```bash
git clone https://github.com/oasis-observatory/oasis-scenario-generator.git
cd oasis-scenario-generator
pip install -r requirements.txt

```

Requirements:

    Python 3.8+

    SQLite3

    (Optional) Ollama or compatible LLM backend

🚀 Usage

Generate a single scenario:
```
python scenario_generator/generate_scenario.py
```
Generate a batch:
```
python scenario_generator/generate_batch.py
```
Output database:
```
data/asi_scenarios.db
```
```

## 📁 Project Structure

scenario_generator/
├── config/
│   └── asi_scenario_schema.json
├── utils/
│   └── abbreviator.py
├── single_asi_scenario.py            # This script generates a scenario based on a JSON schema, samples parameters, and saves the generated scenario to a database.
├── single_asi_batch.py
├── single_asi_database.py
├── multi_asi_scenario.py
├── multi_asi_database.py
└── ...
```
---

## 🧭 Roadmap

- Add multiple LLM agent evaluators
- Strengthen schema validation
- Connect scenarios with precursor signals
- Add narrative quality metrics (Coherence, Novelty, Diversity)

## 🪪 License

Licensed under the MIT License.
© 2025 OASIS Observatory. Open for research and educational use.
