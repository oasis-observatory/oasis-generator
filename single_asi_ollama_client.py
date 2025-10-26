# single_asi_ollama_client.py

import subprocess

def generate_narrative(title, parameters, model_name="llama3"):
    prompt = f"""
You are a foresight analyst. Write a 300-word speculative scenario narrative based on the following ASI system configuration:

Title: {title}

Core Parameters:
{parameters}

Focus on:
- Origin
- Architecture
- Autonomy
- Goal structure
- Risks
- Deployment strategy
- Timeline
    """.strip()

    try:
        process = subprocess.Popen(
            ["ollama", "run", model_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output, error = process.communicate(input=prompt)

        if process.returncode != 0:
            print(f"[❌] Ollama process failed with exit code {process.returncode}")
            print(f"[STDERR]: {error.strip()}")
            return "Narrative generation failed."

        return output.strip()

    except FileNotFoundError:
        return "[❌] Ollama executable not found. Is it installed and in your PATH?"

    except Exception as e:
        return f"[❌] Unexpected error during narrative generation: {str(e)}"
