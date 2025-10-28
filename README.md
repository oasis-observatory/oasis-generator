# Open Artificial SuperIntelligence Scenario Generator v0.1
# OASIS Generator v0.1

Experimental generator producing single-ASI and multi-ASI foresight scenarios using local LLM models.

The **OASIS Generator** is an open-source module for creating narrative simulations of Artificial Superintelligence (ASI) emergence and interaction.
It generates structured scenarios defined by the schema, and stores them in a local SQLite database for later mapping or analysis. 
It can generate both **single-agent (single-ASI)** and **multi-agent (muli-ASI)** scenarios, each accompanied by interpretive narratives and thematic indicators.
It is an experimental tool for producing foresight-style reports on potential futures of Artificial Superintelligence, with potential application in research, educational and creative projects.

This module represents the first step toward the larger OASIS Observatory ecosystem.

**Status:** Alpha — open for testing and conceptual feedback.

✳️ Focus: narrative coherence, scenario diversity, and epistemic transparency.
---

## ✨ Features

- Generate **single-ASI** or **multi-ASI** scenario narratives
- Plug in your preferred LLM backend (Ollama, OpenRouter, Claude, etc.)
- Store and query scenarios using **SQLite3**
- Extensible: connect to precursor data or visualization tools
---

## 📦 Installation

```bash
git clone https://github.com/oasis-observatory/generator.git
cd generator
pip install -r requirements.txt

```

Requirements:

    Python 3.8+

    SQLite3

    (Optional) Ollama or compatible LLM backend

🚀 Usage

Generate a single scenario:
```
python oasis_generator/single_asi_scenario.py
```
Generate a batch:
```
python oasis_generator/single_asi_batch.py
```
Output database:
```
data/asi_scenarios.db
```
```

## 📁 Project Structure

generator/
├── config/
│   └── asi_scenario_schema.json       # JSON schema definition for validating scenario structure
├── utils/
│   └── abbreviator.py                 # Utility to generate shortened ASI scenario titles
├── generate_batch.py                # Batch scenario generation utility
├── parameter_sampler.py               # Defines how scenario parameters are randomly or manually sampled
├── single_asi_scenario.py             # Main script to generate a single ASI scenario
├── single_asi_ollama_client.py        # Connects to local Ollama LLM for single-ASI scenarios
├── single_asi_database.py             # Handles SQLite operations for sinle-ASI scenarios storage at asi_scenarios.db
├── multi_asi_scenario.py              # Generator logic for multi-agent (multi-ASI) scenario narratives based on the single-ASI scenarios from asi_scenarios.db
├── multi_asi_ollama_client.py         # Connects to local Ollama LLM for multi-ASI scenarios
├── multi_asi_database.py              # Handles SQLite operations for multu-ASI scenarios storage at multi_asi_scenarios.db
└── ...
```
---

## 🧭 Roadmap

- [x] Validate results using **JSON Schema**
- [ ] Add multiple LLM agent evaluators
- [ ] Connect scenarios with precursor signals
- [ ] Add narrative quality metrics (Coherence, Novelty, Diversity)

## 🪪 License

Licensed under the MIT License.
© 2025 OASIS Observatory. Open for research and educational use.
