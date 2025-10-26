#generate_scenario.py

import uuid
from datetime import datetime, timezone
from common.schema_loader import load_schema
from parameter_sampler import sample_parameters
from scenario_generator.utils.abbreviator import generate_title_abbreviation
from scenario_generator.ollama_client import generate_narrative
from scenario_generator.database import init_db, save_scenario

# Load the JSON schema
schema = load_schema('asi_scenario_schema.json')

def generate_scenario():
    init_db()

    core = sample_parameters()
    title = generate_title_abbreviation(core)
    scenario_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    narrative = generate_narrative(title, core)

    scenario = {
        "id": scenario_id,
        "title": title,
        "metadata": {
            "created": timestamp,
            "last_updated": timestamp,
            "version": 1,
            "source": "generated"
        },

        # Origins with expanded classification
        "origin": {
            "initial_origin": core["initial_origin"],
            "development_dynamics": core["development_dynamics"]
        },

        # Architecture with topology
        "architecture": {
            "type": core["architecture"],
            "deployment_topology": core["deployment_topology"]
        },

        # Substrate and deployment medium
        "substrate": {
            "type": core["substrate"],
            "deployment_medium": core["deployment_medium"],
            "resilience": core["substrate_resilience"]
        },

        # Oversight with more granularity
        "oversight_structure": {
            "type": core["oversight_type"],
            "effectiveness": core["oversight_effectiveness"],
            "control_surface": core["control_surface"]
        },

        # Core capabilities with normalized agency
        "core_capabilities": {
            "agency_level": core["agency_level"],
            "agency_level_confidence": 0.7,
            "autonomy_degree": core["autonomy_degree"],
            "autonomy_degree_confidence": 0.7,
            "alignment_score": core["alignment_score"],
            "alignment_score_confidence": 0.6,
            "phenomenology_proxy_score": core["phenomenology_proxy_score"]
        },

        # Goals and behavior
        "goals_and_behavior": {
            "stated_goal": core["stated_goal"],
            "mesa_goals": [],
            "opacity": core["opacity"],
            "deceptiveness": core["deceptiveness"],
            "goal_stability": core["goal_stability"]
        },

        # Impact and control, keeping original defaults where appropriate
        "impact_and_control": {
            "impact_domains": ["cyber", "cognitive"],
            "oversight_structure": core["oversight_type"],
            "deployment_strategy": "gradual"
        },

        # Scenario content including narrative and timeline
        "scenario_content": {
            "title": title,
            "narrative": narrative,
            "timeline": {
                "phase_1": {
                    "years": "1970–2100",
                    "description": "Initial development"
                }
            }
        },

        # Quantitative assessment unchanged
        "quantitative_assessment": {
            "probability": {
                "emergence_probability": 0.4,
                "detection_confidence": 0.5,
                "projection_confidence": 0.6,
                "trend": "stable",
                "last_update_reason": "initial generation"
            },
            "risk_assessment": {
                "existential": {"score": 3, "weight": 0.6},
                "economic": {"score": 2, "weight": 0.2},
                "social": {"score": 3, "weight": 0.1},
                "political": {"score": 2, "weight": 0.1}
            }
        },

        # Observable evidence placeholder
        "observable_evidence": {
            "key_indicators": [],
            "supporting_signals": []
        }
    }

    save_scenario(scenario)
    print(f"✅ Scenario '{title}' saved to database.")

if __name__ == "__main__":
    generate_scenario()
