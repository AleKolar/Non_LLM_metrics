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

