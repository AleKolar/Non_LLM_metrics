# src/services/metrics/ai_service.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def analyze_metrics(metrics: dict) -> str:
    prompt = f"""
    Ты — Senior QA Engineer. Мы анализируем критерии качества модели ИИ по non-LLM метрикам 
    (Accuracy, Precision, Recall, F1, RR, MRR). 
    На основании полученных числовых значений каждой метрики дай краткий, строгий анализ 
    качества выдачи поисковой модели.

    Метрики:
    - Accuracy: {metrics['accuracy']}
    - Precision: {metrics['precision']}
    - Recall: {metrics['recall']}
    - F1-score: {metrics['f1']}
    - RR: {metrics['rr']}
    - MRR: {metrics['mrr']}

    Ответ напиши на русском, 3-4 предложения:
    1. Общая оценка качества.
    2. Сильные стороны.
    3. Слабые стороны.
    4. Рекомендации по улучшению (если есть).
    Не отвлекайся на посторонние темы. Говори только о метриках и выдаче модели.
    """

    if not API_KEY:
        return "Ошибка: OPENROUTER_API_KEY не задан."

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/free", # можно пробовать с конкретными: "model": "deepseek/deepseek-chat" ; "model": "meta-llama/llama-3.1-8b-instruct" ; "model": "openai/gpt-4o-mini"
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 250
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Ошибка OpenRouter: {response.status_code} {response.text}"

