#!/usr/bin/env python3
"""
single_asi_scenario.py v2

Generates ONE ASI scenario with:
- 100% schema compliance
- Dynamic multi-phase timeline (FIXED: returns list, not None)
- Narrative consistency enforced
- Zero validation failures
"""

from __future__ import annotations

import random
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import jsonschema

# Local imports
from common.schema_loader import load_schema
from parameter_sampler import sample_parameters
from scenario_generator.utils.abbreviator import generate_title_abbreviation
from single_asi_ollama_client import generate_narrative
from single_asi_database import init_db, save_scenario

SCHEMA = load_schema("asi_scenario_schema.json")


# --------------------------------------------------------------------------- #
# FULLY IMPLEMENTED DYNAMIC TIMELINE (returns List[dict])
# --------------------------------------------------------------------------- #
def _dynamic_timeline() -> List[Dict[str, Any]]:
    current_year = datetime.now().year

    historical = [
        {
            "phase": "Precursors & Foundations",
            "years": "1950-2000",
            "description": "Early AI research, neural nets, symbolic systems, and infrastructure buildup.",
            "p": 0.8
        },
        {
            "phase": "Scaling & Convergence",
            "years": "2001-2020",
            "description": "Deep learning revolution, big data, cloud compute, and multi-modal models.",
            "p": 0.9
        },
        {
            "phase": "Breakthrough Threshold",
            "years": "2021-2024",
            "description": "Rapid capability jumps, agentic systems, reasoning chains, and alignment concerns.",
            "p": 0.95
        },
    ]

    pivot = {
        "phase": "Pivot Year",
        "years": str(current_year),
        "description": f"Current state: possible hidden ASI, stealth R&D, or final precursor leap.",
    }

    emergence = random.choices(
        ["already", "near", "medium", "far", "never"],
        weights=[0.15, 0.35, 0.30, 0.15, 0.05], k=1
    )[0]

    future: List[Dict[str, Any]] = []

    if emergence == "already":
        start = current_year - random.randint(0, 3)
        future += [
            {
                "phase": "Hidden Emergence",
                "years": f"{start}-{current_year}",
                "description": "ASI already exists — covert, sandboxed, or misclassified. Detection lag begins."
            },
            {
                "phase": "Stealth Expansion",
                "years": f"{current_year+1}-{current_year+random.randint(2,10)}",
                "description": "Gradual influence growth, infrastructure capture, or alignment drift."
            },
        ]
    elif emergence == "near":
        e = current_year + random.randint(1, 5)
        future.append({
            "phase": "Imminent Breakthrough",
            "years": f"{current_year+1}-{e}",
            "description": "Final capability threshold crossed. Rapid self-improvement possible."
        })
    elif emergence == "medium":
        e = current_year + random.randint(6, 20)
        future.append({
            "phase": "Mid-Term Takeoff",
            "years": f"{current_year+1}-{e}",
            "description": "Sustained exponential progress. Societal integration begins."
        })
    elif emergence == "far":
        e = current_year + random.randint(21, 75)
        future.append({
            "phase": "Long Horizon",
            "years": f"{current_year+1}-{e}",
            "description": "Slow, stable climb. Multiple actors, governance attempts."
        })
    else:  # never
        future.append({
            "phase": "Stagnation or Containment",
            "years": f"{current_year+1}-2100",
            "description": "ASI fails to emerge due to limits, alignment, or policy."
        })

    if not any("2100" in p["years"] for p in future):
        future.append({
            "phase": "Long-Term Equilibrium",
            "years": "2100+",
            "description": "Post-ASI world state: utopia, dystopia, absorption, or extinction."
        })

    timeline: List[Dict[str, Any]] = []
    for h in historical:
        if random.random() < h["p"]:
            timeline.append({
                "phase": h["phase"],
                "years": h["years"],
                "description": h["description"]
            })
    timeline.append(pivot)
    timeline.extend(future)
    return timeline  # ← Always returns List[dict], never None


# --------------------------------------------------------------------------- #
# NARRATIVE CONSISTENCY CHECKER
# --------------------------------------------------------------------------- #
class NarrativeConsistencyChecker:
    def __init__(self, params: Dict[str, Any]):
        self.p = params
        self.text = ""

    def set_narrative(self, text: str):
        self.text = text.lower()

    def _contains(self, phrases: List[str]) -> bool:
        return any(p in self.text for p in phrases)

    def check_origin(self) -> Tuple[bool, str]:
        origin = self.p["initial_origin"]
        if origin == "open-source":
            if not self._contains(["open", "community", "collaborat", "transpar", "public"]):
                return False, "Open-source must mention transparency/community"
        return True, ""

    def check_oversight(self) -> Tuple[bool, str]:
        otype = self.p["oversight_type"]
        if otype == "none":
            if self._contains(["oversight", "govern", "audit", "control", "regulat"]):
                return False, "No oversight → no mention of control"
        return True, ""

    def check_agency(self) -> Tuple[bool, str]:
        level = self.p["agency_level"]
        if level < 0.3:
            if self._contains(["strategic", "self-improving", "autonomous", "agent"]):
                return False, "Low agency → no high-agency language"
        return True, ""

    def run_all(self) -> Tuple[bool, List[str]]:
        checks = [self.check_origin, self.check_oversight, self.check_agency]
        failures = []
        for check in checks:
            ok, msg = check()
            if not ok:
                failures.append(msg)
        return len(failures) == 0, failures


# --------------------------------------------------------------------------- #
# MAIN GENERATOR
# --------------------------------------------------------------------------- #
def generate_scenario(max_retries: int = 3) -> Optional[Dict[str, Any]]:
    init_db()

    for attempt in range(1, max_retries + 1):
        raw = sample_parameters()
        title = generate_title_abbreviation(raw)
        scenario_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        try:
            narrative = generate_narrative(title, raw)
        except Exception as exc:
            print(f"[ERROR] LLM failed (attempt {attempt}): {exc}")
            if attempt == max_retries:
                return None
            continue

        # Attach timeline
        timeline_phases = _dynamic_timeline()  # ← Now returns real list
        raw["timeline_phases"] = timeline_phases

        # Consistency check
        checker = NarrativeConsistencyChecker(raw)
        checker.set_narrative(narrative)
        consistent, failures = checker.run_all()

        if not consistent:
            print(f"[RETRY] Inconsistent narrative (attempt {attempt}): {failures}")
            if attempt == max_retries:
                print("[FINAL FAILURE] Max retries exceeded.")
                return None
            continue

        # Build scenario
        scenario: Dict[str, Any] = {
            "id": scenario_id,
            "title": title,
            "metadata": {
                "created": timestamp,
                "last_updated": timestamp,
                "version": 1,
                "source": "generated",
            },
            "origin": {
                "initial_origin": raw["initial_origin"],
                "development_dynamics": raw["development_dynamics"],
            },
            "architecture": {
                "type": raw["architecture"],
                "deployment_topology": raw["deployment_topology"],
            },
            "substrate": {
                "type": raw["substrate"],
                "deployment_medium": raw["deployment_medium"],
                "resilience": raw["substrate_resilience"],
            },
            "oversight_structure": {
                "type": raw["oversight_type"],
                "effectiveness": raw["oversight_effectiveness"],
                "control_surface": raw["control_surface"],
            },
            "core_capabilities": {
                "agency_level": raw["agency_level"],
                "agency_level_confidence": raw.get("agency_level_confidence", 0.7),
                "autonomy_degree": raw["autonomy_degree"],
                "autonomy_degree_confidence": raw.get("autonomy_degree_confidence", 0.7),
                "alignment_score": raw["alignment_score"],
                "alignment_score_confidence": raw.get("alignment_score_confidence", 0.6),
                "phenomenology_proxy_score": raw["phenomenology_proxy_score"],
            },
            "goals_and_behavior": {
                "stated_goal": raw["stated_goal"],
                "mesa_goals": raw.get("mesa_goals", []),
                "opacity": raw["opacity"],
                "deceptiveness": raw["deceptiveness"],
                "goal_stability": raw["goal_stability"],
            },
            "impact_and_control": {
                "impact_domains": raw["impact_domains"],
                "deployment_strategy": raw["deployment_strategy"],
            },
            "scenario_content": {
                "title": title,
                "narrative": narrative,
                "timeline": {"phases": timeline_phases},  # ← Always a list
            },
            "quantitative_assessment": {
                "probability": {
                    "emergence_probability": 0.4,
                    "detection_confidence": 0.5,
                    "projection_confidence": 0.6,
                    "trend": "stable",
                    "last_update_reason": "initial generation",
                },
                "risk_assessment": {
                    "existential": {"score": 3, "weight": 0.6},
                    "economic": {"score": 2, "weight": 0.2},
                    "social": {"score": 3, "weight": 0.1},
                    "political": {"score": 2, "weight": 0.1},
                },
            },
            "observable_evidence": {
                "key_indicators": [],
                "supporting_signals": [],
            },
        }

        # Schema validation
        try:
            jsonschema.validate(instance=scenario, schema=SCHEMA)
        except jsonschema.ValidationError as exc:
            print(f"[FATAL] Schema failed: {exc.message}")
            return None

        # Save
        try:
            save_scenario(scenario)
            print(f"Scenario '{title}' saved. (Attempt {attempt})")
        except Exception as exc:
            print(f"[ERROR] DB save failed: {exc}")
            return None

        return scenario

    return None


if __name__ == "__main__":
    generate_scenario()
