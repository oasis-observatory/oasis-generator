# single_asi_ollama_client.py v3
"""
Multi-model Ollama client for OASIS ASI scenario generation.
Supports model fallbacks, timeouts, and timeline enforcement.
"""

import subprocess
import logging
import random
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ModelStrategy(Enum):
    PRIORITY = "priority"      # Try models in order
    RANDOM = "random"          # Pick one at random
    ROUND_ROBIN = "round_robin"  # Cycle through list


@dataclass
class ModelConfig:
    name: str
    timeout: int = 60
    max_retries: int = 1


# === CONFIGURABLE MODEL LIST ===
# Add/remove models here. Order matters for PRIORITY.
AVAILABLE_MODELS = [
    ModelConfig("llama3", timeout=300),
    ModelConfig("llama3:8b", timeout=300),
    ModelConfig("mistral:7b", timeout=300),
    ModelConfig("phi3:medium", timeout=300),
    ModelConfig("gemma2:9b", timeout=300),
]

# === SYSTEM PROMPT (ENFORCED) ===
SYSTEM_PROMPT = """
You are OASIS-7, a strategic foresight analyst for the Open Artificial Superintelligence Scenario Observatory.
Write a 350-word speculative scenario in third-person, formal, analytical tone.

Structure:
1. Origin & Development
2. Architecture & Deployment
3. Emergence & Autonomy
4. Risks & Outcome

CRITICAL: You MUST follow this exact timeline:
{timeline}

NEVER invent new years or phases. Use only the phases and years above.
""".strip()

USER_TEMPLATE = """
Title: {title}

Parameters:
{formatted_params}

Timeline:
{timeline}

Write the scenario now.
""".strip()


# === HELPER: FORMAT PARAMETERS ===
def _format_params(params: Dict[str, Any]) -> str:
    ignore = {"timeline_phases", "mesa_goals"}
    lines = []
    for k, v in params.items():
        if k in ignore or v is None:
            continue
        key = k.replace('_', ' ').title()
        if isinstance(v, list):
            val = ", ".join(map(str, v))
        else:
            val = str(v)
        lines.append(f"- {key}: {val}")
    return "\n".join(lines) if lines else "- No parameters provided"


# === HELPER: FORMAT TIMELINE ===
def _format_timeline(phases: List[Dict[str, str]]) -> str:
    return "\n".join([f"- {p['phase']}: {p['years']}" for p in phases])


# === CORE: RUN SINGLE MODEL ===
def _run_model(
    model: ModelConfig,
    prompt: str
) -> Tuple[bool, str, Optional[str]]:
    try:
        logger.debug(f"Running model: {model.name} (timeout={model.timeout}s)")
        process = subprocess.Popen(
            ["ollama", "run", model.name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        stdout, stderr = process.communicate(input=prompt, timeout=model.timeout)

        if process.returncode != 0:
            error = f"{model.name} failed (code {process.returncode}): {stderr.strip()}"
            logger.error(error)
            return False, "", error

        narrative = stdout.strip()
        if len(narrative) < 100:
            return False, "", f"{model.name}: Output too short ({len(narrative)} chars)"

        return True, narrative, None

    except FileNotFoundError:
        error = "Ollama not found in PATH"
        logger.error(error)
        return False, "", error
    except subprocess.TimeoutExpired:
        process.kill()
        error = f"{model.name}: Timed out after {model.timeout}s"
        logger.warning(error)
        return False, "", error
    except Exception as e:
        error = f"{model.name}: {str(e)}"
        logger.error(error)
        return False, "", error


# === MAIN: GENERATE NARRATIVE WITH FALLBACKS ===
def generate_narrative(
    title: str,
    parameters: Dict[str, Any],
    timeline_phases: List[Dict[str, str]],
    strategy: ModelStrategy = ModelStrategy.PRIORITY,
    preferred_model: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
    """
    Generate narrative with model fallbacks.

    Returns:
        (success: bool, narrative: str|None, model_used: str|None, error: str|None)
    """
    models_to_try = []

    if preferred_model:
        # Try preferred first
        config = next((m for m in AVAILABLE_MODELS if m.name == preferred_model), None)
        if config:
            models_to_try.append(config)

    # Build fallback list
    if strategy == ModelStrategy.PRIORITY:
        models_to_try.extend(AVAILABLE_MODELS)
    elif strategy == ModelStrategy.RANDOM:
        models_to_try = random.sample(AVAILABLE_MODELS, len(AVAILABLE_MODELS))
    elif strategy == ModelStrategy.ROUND_ROBIN:
        # Simple round-robin via global index
        idx = getattr(generate_narrative, "_rr_index", 0)
        models_to_try = AVAILABLE_MODELS[idx:] + AVAILABLE_MODELS[:idx]
        generate_narrative._rr_index = (idx + 1) % len(AVAILABLE_MODELS)

    # Dedupe
    seen = set()
    models_to_try = [m for m in models_to_try if m.name not in seen and not (seen.add(m.name))]

    if not models_to_try:
        return False, None, None, "No models available"

    # Format prompt
    formatted_params = _format_params(parameters)
    timeline_str = _format_timeline(timeline_phases)
    full_prompt = f"{SYSTEM_PROMPT.format(timeline=timeline_str)}\n\n{USER_TEMPLATE.format(title=title, formatted_params=formatted_params, timeline=timeline_str)}"

    # Try models
    for model in models_to_try:
        for attempt in range(model.max_retries):
            success, narrative, error = _run_model(model, full_prompt)
            if success:
                logger.info(f"Narrative generated with {model.name}")
                return True, narrative, model.name, None
            else:
                logger.warning(f"Attempt {attempt+1} failed with {model.name}: {error}")

    final_error = "All models failed"
    logger.error(final_error)
    return False, None, None, final_error
