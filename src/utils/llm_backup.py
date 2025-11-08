"""
Lightweight Gemini client for text generation
Simple interface with retry logic and error handling
"""

import os
import time
import google.generativeai as genai

GEN_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")


def _configure():
    """
    Configure Gemini API and return model instance
    
    Returns:
        Configured GenerativeModel instance
        
    Raises:
        RuntimeError: If GOOGLE_API_KEY not set in environment
    """
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GOOGLE_API_KEY not set")
    genai.configure(api_key=key)
    return genai.GenerativeModel(GEN_MODEL)


def generate_text(system_prompt: str, user_prompt: str) -> str:
    """
    Generate text using Gemini with retry logic
    
    Args:
        system_prompt: System instruction/context
        user_prompt: User's actual prompt
        
    Returns:
        Generated text response (trimmed)
        
    Raises:
        Exception: If all retry attempts fail
    """
    model = _configure()
    attempt = 0
    
    while True:
        try:
            resp = model.generate_content([
                {"role": "system", "parts": [system_prompt]},
                {"role": "user", "parts": [user_prompt]}
            ])
            return (resp.text or "").strip()
        except Exception as e:
            attempt += 1
            if attempt >= 3:
                raise
            # Exponential backoff: 1.5s, 3s
            time.sleep(1.5 * attempt)
