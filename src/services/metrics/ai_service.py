# src/services/metrics/ai_service.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")


def analyze_metrics(metrics: dict) -> str:
    prompt = f"""
    Ты QA Senior. Проанализируй качество поисковой системы.

    Accuracy: {metrics['accuracy']}
    Precision: {metrics['precision']}
    Recall: {metrics['recall']}
    F1: {metrics['f1']}
    RR: {metrics['rr']}
    MRR: {metrics['mrr']}

    Дай краткий анализ."""

    if not API_KEY:
        return "Ошибка: OPENROUTER_API_KEY не задан."

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-v4-flash:free",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Ошибка OpenRouter: {response.status_code} {response.text}"
