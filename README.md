# Non_LLM_metrics
Automatic calculation of non LLM metrics of the AI model

Сервис для расчёта non-LLM метрик (Accuracy, Precision, Recall, F1, RR, MRR) и AI-анализа качества поисковой выдачи.

## Технологии
- Python 3.12, FastAPI, Pydantic
- HTML/CSS/JavaScript (vanilla)
- OpenRouter API (DeepSeek)

## Запуск
1. Клонировать репозиторий
2. Создать виртуальное окружение и установить зависимости (в данном случае requirements.txt - избыточен (с предыдущего проекта), 
но обеспечивает работоспособность и не подвергает систему рискам) 
3. Создать `.env` с ключом `OPENROUTER_API_KEY`
4. Выполнить `uvicorn main:app --reload`

Открыть в браузере http://127.0.0.1:8000
