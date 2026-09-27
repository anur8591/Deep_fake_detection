import ollama
import base64


def analyze_image(image_bytes):

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
You are assisting a video deepfake detection system.

Analyze this video frame carefully.

Look for visual signs such as:
- unnatural facial features
- face blending artifacts
- inconsistent skin texture
- strange eyes or mouth
- lighting inconsistencies
- unnatural edges around the face
- obvious AI-generated/manipulated appearance

IMPORTANT:
You are providing a SECOND OPINION only.
Do not claim certainty.

Return only this format:

VERDICT: REAL or FAKE
CONFIDENCE: number from 0 to 100
REASON: short explanation
"""

    results = {}

    # ---------------- LLaVA ----------------

    try:

        response = ollama.generate(
            model="llava:latest",
            prompt=prompt,
            images=[image_base64]
        )

        results["llava"] = response["response"]

    except Exception as e:

        results["llava"] = f"ERROR: {str(e)}"


    # ---------------- Gemma 3 ----------------

    try:

        response = ollama.generate(
            model="gemma3:4b",
            prompt=prompt,
            images=[image_base64]
        )

        results["gemma3"] = response["response"]

    except Exception as e:

        results["gemma3"] = f"ERROR: {str(e)}"


    return results