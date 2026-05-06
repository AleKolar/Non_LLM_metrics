# import os
# import requests
# from dotenv import load_dotenv
#
# load_dotenv()
#
# API_KEY = os.getenv("GEMINI_API_KEY")
# print(API_KEY)
#
# def analyze_metrics(metrics: dict) -> str:
#     prompt = f"""
# Ты QA Senior. Проанализируй качество поисковой системы.
#
# Accuracy: {metrics['accuracy']}
# Precision: {metrics['precision']}
# Recall: {metrics['recall']}
# F1: {metrics['f1']}
# RR: {metrics['rr']}
# MRR: {metrics['mrr']}
#
# Дай краткий анализ."""
#
#     if not API_KEY:
#         return "Ошибка: GEMINI_API_KEY не задан. Проверьте файл .env."
#
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
#     headers = {"Content-Type": "application/json"}
#     payload = {
#         "contents": [
#             {"parts": [{"text": prompt}]}
#         ]
#     }
#
#     try:
#         response = requests.post(url, headers=headers, json=payload, timeout=30)
#         response.raise_for_status()
#         data = response.json()
#         return data["candidates"][0]["content"]["parts"][0]["text"]
#     except requests.exceptions.RequestException as e:
#         return f"Ошибка сети или HTTP: {e}"
#     except (KeyError, IndexError) as e:
#         return f"Некорректный ответ API: {response.text}"

# tests/test_ai_real.py
import pytest
from src.services.metrics.ai_service import analyze_metrics

# Обязательно пометим маркером, чтобы случайно не запускать в быстром CI каждый раз
@pytest.mark.real_ai
def test_openrouter_connectivity_and_response():
    """Проверяет, что реальный AI-сервис доступен и возвращает осмысленный текст."""
    sample_metrics = {
        "accuracy": 0.85,
        "precision": 0.78,
        "recall": 0.92,
        "f1": 0.85,
        "rr": 1.0,
        "mrr": 0.75
    }

    result = analyze_metrics(sample_metrics)

    # Базовая проверка: результат — строка, не пустая, не содержит ошибок
    assert isinstance(result, str), "Ответ должен быть строкой"
    assert len(result) > 0, "Ответ не должен быть пустым"

    # Убеждаемся, что это не сообщение об ошибке
    assert not result.startswith("Ошибка"), f"Получена ошибка: {result}"

    # Дополнительно можно проверить, что упоминаются ключевые метрики
    # (это опционально, но даёт уверенность, что модель действительно анализировала)
    assert any(word in result.lower() for word in ["accuracy", "precision", "recall"]), \
        "Ответ не содержит упоминаний метрик"