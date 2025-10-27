# single_asi_ollama_client.py v2

import subprocess
import json
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are OASIS-7, a strategic foresight analyst for the Open Artificial Superintelligence Scenario Observatory.
Write a 300-word speculative scenario in third-person, formal, analytical tone.

Structure:
1. Origin & Development
2. Architecture & Deployment
3. Emergence & Autonomy
4. Risks & Outcome

CRITICAL: You MUST follow this exact timeline:
{timeline}

NEVER invent new years or phases.
""".strip()

USER_TEMPLATE = """
Title: {title}

Parameters:
{formatted_params}

Timeline:
{timeline}

Write the scenario now.
""".strip()


def _format_params(params: dict) -> str:
    return "\n".join([
        f"- {k.replace('_', ' ').title()}: {v}"
        for k, v in params.items()
        if k != "timeline_phases"
    ])


def _format_timeline(phases: list) -> str:
    return "\n".join([f"- {p['phase']}: {p['years']}" for p in phases])


def generate_narrative(
    title: str,
    parameters: dict,
    timeline_phases: list,
    model_name: str = "llama3",
    timeout: int = 60
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Returns: (success, narrative, error)
    """
    formatted_params = _format_params(parameters)
    timeline_str = _format_timeline(timeline_phases)

    prompt = f"{SYSTEM_PROMPT.format(timeline=timeline_str)}\n\n{USER_TEMPLATE.format(title=title, formatted_params=formatted_params, timeline=timeline_str)}"

    try:
        process = subprocess.Popen(
            ["ollama", "run", model_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        stdout, stderr = process.communicate(input=prompt, timeout=timeout)

        if process.returncode != 0:
            error = f"Ollama failed (code {process.returncode}): {stderr.strip()}"
            logger.error(error)
            return False, None, error

        narrative = stdout.strip()
        if len(narrative) < 100:
            return False, None, "Narrative too short"

        return True, narrative, None

    except FileNotFoundError:
        error = "Ollama not found in PATH"
        logger.error(error)
        return False, None, error
    except subprocess.TimeoutExpired:
        process.kill()
        error = "Ollama timed out"
        logger.error(error)
        return False, None, error
    except Exception as e:
        error = f"Unexpected error: {str(e)}"
        logger.error(error)
        return False, None, error
