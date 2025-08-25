# app/llm_integration.py
import os
import asyncio
from typing import Dict, Any
from app.config import settings
from app.logger import logger



async def analyze_text_with_llm(text: str) -> Dict[str, Any]:
    """
    Analyze text with an LLM (placeholder).
    Returns classification, confidence, reasoning, and raw response.
    """
   
    lowered = text.lower()
    score = 0.0
    if any(w in lowered for w in ["kill", "bomb", "hate", "rape"]):
        classification = "toxic"
        score = 0.95
    elif any(w in lowered for w in ["buy now", "click here", "subscribe"]):
        classification = "spam"
        score = 0.86
    elif any(w in lowered for w in ["idiot", "stupid", "dumb"]):
        classification = "harassment"
        score = 0.75
    else:
        classification = "safe"
        score = 0.99

    reasoning = f"Simple heuristic classification: '{classification}' detected with score {score}."
    llm_response = {"model": "heuristic-stub", "raw": text[:400]}

    # Simulate I/O latency
    await asyncio.sleep(0.1)
    logger.info("LLM analysis complete (stub).")
    return {
        "classification": classification,
        "confidence": float(score),
        "reasoning": reasoning,
        "llm_response": llm_response,
    }


async def call_openai_real(text: str) -> Dict[str, Any]:
    """
    Example function to show how to call OpenAI (not executed in the stub).
    Keep as reference to replace the stub later.
    """
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not configured")

    raise NotImplementedError("Replace call_openai_real with actual OpenAI call.")
