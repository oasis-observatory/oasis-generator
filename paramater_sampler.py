# parameter_sampler.py

import random

def sample_parameters():

    return {
        # Origin split into source and development dynamics
        "initial_origin": random.choice([
            "state", "corporate", "academic", "open-source", "individual", "military"
        ]),
        "development_dynamics": random.choice([
            "engineered", "emergent", "hybrid"
        ]),

        # Architecture with possibility for modular and deployment topology
        "architecture": random.choice([
            "monolithic", "swarm", "federated", "modular", "layered"
        ]),
        "deployment_topology": random.choice([
            "centralized", "distributed", "edge", "hybrid"
        ]),

        # Oversight split into type, effectiveness, and control surface
        "oversight_type": random.choice([
            "corporate", "governmental", "multi-stakeholder", "open-source", "none"
        ]),
        "oversight_effectiveness": random.choice([
            "strong", "partial", "ineffective", "collapsed"
        ]),
        "control_surface": random.choice([
            "legal", "technical", "market", "social", "unknown"
        ]),

        # Substrate classification
        "substrate": random.choice([
            "conventional_compute", "neuromorphic", "quantum", "biological", "hybrid", "unknown"
        ]),
        "deployment_medium": random.choice([
            "cloud", "edge", "embedded", "space-based", "ubiquitous", "virtual"
        ]),
        "substrate_resilience": random.choice([
            "fragile", "redundant", "self-repairing"
        ]),

        # Core capabilities and behavior, largely as before but with normalized agency level
        "agency_level": round(random.uniform(0.0, 1.0), 2),
        "autonomy_degree": random.choice(["controlled", "partial", "full"]),
        "alignment_score": round(random.uniform(0.0, 1.0), 2),
        "phenomenology_proxy_score": round(random.uniform(0.0, 1.0), 2),

        # Goals and behavior
        "stated_goal": random.choice([
            "human-welfare", "profit", "survival", "exploration", "other"
        ]),
        "opacity": round(random.uniform(0.0, 1.0), 2),
        "deceptiveness": round(random.uniform(0.0, 1.0), 2),
        "goal_stability": random.choice([
            "fixed", "modifiable", "dynamic"
        ])
    }
