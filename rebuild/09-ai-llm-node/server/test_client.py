#!/usr/bin/env python3
"""
Test client to verify AI Cortex LLM endpoint and AGY Gemini Grounding.
"""
import requests
import json
import sys

API_URL = "http://192.168.0.235:8000/v1/chat/completions"

def test_query(prompt: str, require_verification: bool = True):
    print(f"\n--- Testing Query ---")
    print(f"Prompt: {prompt}")
    print(f"Grounding with AGY Gemini: {require_verification}")

    payload = {
        "model": "agy-grounded",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "require_verification": require_verification
    }

    try:
        resp = requests.post(API_URL, json=payload, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            reply = data["choices"][0]["message"]["content"]
            model_used = data.get("model", "unknown")
            print(f"Model: {model_used}")
            print(f"Response:\n{reply}\n")
        else:
            print(f"Error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_query("What was the exact final score and scorers for today's Liverpool Premier League game?")
