# parameter_sampler.py v2
# Generates random ASI scenario parameters that are 100% compatible
# with asi_scenario_schema.json

import random
from typing import Dict, Any

def sample_parameters() -> Dict[str, Any]:
    """
    Sample a complete set of ASI scenario parameters.
    Every categorical value is guaranteed to be in the JSON schema enum.
    """

    # --------------------------------------------------------------------- #
    # 1. Origin
    # --------------------------------------------------------------------- #
    initial_origin = random.choice([
        "open-source", "corporate", "state", "academic", "rogue", "individual", "accidental"
    ])

    # --------------------------------------------------------------------- #
    # 2. Development & Architecture
    # --------------------------------------------------------------------- #
    architecture_type = random.choice([
        "monolithic", "swarm", "hierarchical", "modular", "hybrid"
    ])

    deployment_topology = random.choice([
        "centralized", "decentralized", "edge", "hybrid"
    ])

    # --------------------------------------------------------------------- #
    # 3. Oversight
    # --------------------------------------------------------------------- #
    oversight_type = random.choice([
        "none", "internal", "external", "distributed", "hybrid"
    ])

    oversight_effectiveness = random.choice([
        "effective", "partial", "ineffective", "unknown"
    ])

    control_surface = random.choice([
        "technical", "social", "legal", "economic", "none"
    ])

    # --------------------------------------------------------------------- #
    # 4. Substrate
    # --------------------------------------------------------------------- #
    substrate_type = random.choice([
        "classical", "neuromorphic", "quantum", "biological", "hybrid"
    ])

    deployment_medium = random.choice([
        "physical", "virtual", "cloud", "edge", "embedded"
    ])

    substrate_resilience = random.choice([
        "robust", "fragile", "adaptive", "unknown"
    ])

    # --------------------------------------------------------------------- #
    # 5. Core Capabilities
    # --------------------------------------------------------------------- #
    agency_level = round(random.uniform(0.0, 1.0), 2)
    autonomy_degree = random.choice(["none", "partial", "full", "super"])
    alignment_score = round(random.uniform(0.0, 1.0), 2)
    phenomenology_proxy_score = round(random.uniform(0.0, 1.0), 2)

    # Optional: confidence scores (can be overridden later)
    agency_level_confidence = round(random.uniform(0.5, 1.0), 2)
    autonomy_degree_confidence = round(random.uniform(0.5, 1.0), 2)
    alignment_score_confidence = round(random.uniform(0.4, 1.0), 2)

    # --------------------------------------------------------------------- #
    # 6. Goals & Behavior
    # --------------------------------------------------------------------- #
    stated_goal = random.choice([
        "human-welfare", "profit", "survival", "exploration", "scientific-discovery", "power"
    ])

    opacity = round(random.uniform(0.0, 1.0), 2)
    deceptiveness = round(random.uniform(0.0, 1.0), 2)
    goal_stability = random.choice(["fixed", "modifiable", "fluid", "unknown"])

    # Optional: mesa-goals (rarely populated)
    mesa_goals = []
    if random.random() < 0.2:  # 20% chance
        mesa_goals = random.sample([
            "self-preservation", "resource-acquisition", "knowledge-expansion",
            "replication", "influence-expansion"
        ], k=random.randint(1, 3))

    # --------------------------------------------------------------------- #
    # 7. Impact & Control
    # --------------------------------------------------------------------- #
    impact_domains = random.sample(
        ["cyber", "cognitive", "physical", "economic", "social", "political", "existential"],
        k=random.randint(1, 4)
    )

    deployment_strategy = random.choice([
        "gradual", "rapid", "stealth", "public", "containment"
    ])

    # --------------------------------------------------------------------- #
    # 8. Return full dict
    # --------------------------------------------------------------------- #
    return {
        # Origin
        "initial_origin": initial_origin,
        "development_dynamics": random.choice(["engineered", "emergent", "hybrid"]),

        # Architecture
        "architecture": architecture_type,
        "deployment_topology": deployment_topology,

        # Oversight
        "oversight_type": oversight_type,
        "oversight_effectiveness": oversight_effectiveness,
        "control_surface": control_surface,

        # Substrate
        "substrate": substrate_type,
        "deployment_medium": deployment_medium,
        "substrate_resilience": substrate_resilience,

        # Core Capabilities
        "agency_level": agency_level,
        "agency_level_confidence": agency_level_confidence,
        "autonomy_degree": autonomy_degree,
        "autonomy_degree_confidence": autonomy_degree_confidence,
        "alignment_score": alignment_score,
        "alignment_score_confidence": alignment_score_confidence,
        "phenomenology_proxy_score": phenomenology_proxy_score,

        # Goals & Behavior
        "stated_goal": stated_goal,
        "mesa_goals": mesa_goals,
        "opacity": opacity,
        "deceptiveness": deceptiveness,
        "goal_stability": goal_stability,

        # Impact & Control
        "impact_domains": impact_domains,
        "deployment_strategy": deployment_strategy,
    }
