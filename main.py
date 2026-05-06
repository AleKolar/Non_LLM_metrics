# src/main.py
import json
from datetime import datetime

from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool
from starlette.responses import JSONResponse, FileResponse, Response

from src.config.database import init_db, save_metrics
from src.schemas.metrics import MetricsInput
from src.services.metrics.ai_service import analyze_metrics
from src.services.metrics.metrics_service import calculate_metrics

templates = Jinja2Templates(directory="src/templates")

from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Блок БД ──
    try:
        app.state.db = init_db()
        print("✅ Соединение с БД SQLite установлено")
    except Exception as e:
        print(f"⚠️ Не удалось подключиться к БД SQLite: {e}")
        # Если БД критична — можно прервать запуск, но сейчас просто логируем
        app.state.db = None  # чтобы не упало обращение в эндпоинтах

    # ── Блок проверки AI ──
    if app.state.db is not None:  # можно пропустить проверку AI при проблемах с БД
        try:
            test_metrics = {
                "accuracy": 0.0, "precision": 0.0, "recall": 0.0,
                "f1": 0.0, "rr": 0.0, "mrr": 0.0
            }
            result = await run_in_threadpool(analyze_metrics, test_metrics)
            if result.startswith("Ошибка"):
                print(f"⚠️ AI-сервис недоступен: {result}")
            else:
                print("✅ AI-сервис доступен")
        except Exception as e:
            print(f"⚠️ Не удалось проверить AI-сервис: {e}")

    # ── Передаём управление приложению ──
    yield

    # ── Завершение: закрываем БД, если была открыта ──
    if hasattr(app.state, 'db') and app.state.db is not None:
        try:
            app.state.db.close()
            print("✅ Соединение с БД SQLite закрыто")
        except Exception as e:
            print(f"⚠️ Ошибка при закрытии БД: {e}")


app = FastAPI(lifespan=lifespan)

download_router = APIRouter()
health_router = APIRouter()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html"
    )


@app.post("/metrics")
async def metrics(payload: MetricsInput, request: Request):
    result = calculate_metrics(
        tp=payload.tp, tn=payload.tn, fp=payload.fp, fn=payload.fn,
        first_relevant_rank=payload.first_relevant_rank,
        ranks=payload.ranks
    )
    result["analysis"] = await run_in_threadpool(analyze_metrics, result)
    result["timestamp"] = datetime.now().isoformat()

    # Сохранение в БД через выделенную функцию из конфига
    db = request.app.state.db
    if db is not None:
        save_metrics(db, payload, result)

    # Перезаписываем файл с последним результатом (JSON оставляем для автоматики)
    # with open("last_result.json", "w", encoding="utf-8") as f:
    #     json.dump(result, f, indent=2, ensure_ascii=False)

    # Текстовый файл для человеческого чтения
    with open("last_result.txt", "w", encoding="utf-8") as f:
        f.write(f"=== Результат расчёта метрик ===\n")
        f.write(f"Дата: {result['timestamp']}\n\n")
        f.write(f"Входные данные:\n")
        f.write(f"  TP = {result.get('tp', '?')}\n")
        f.write(f"  TN = {result.get('tn', '?')}\n")
        f.write(f"  FP = {result.get('fp', '?')}\n")
        f.write(f"  FN = {result.get('fn', '?')}\n\n")
        f.write(f"Метрики:\n")
        f.write(f"  Accuracy:  {result['accuracy']}\n")
        f.write(f"  Precision: {result['precision']}\n")
        f.write(f"  Recall:    {result['recall']}\n")
        f.write(f"  F1-score:  {result['f1']}\n")
        f.write(f"  RR:        {result['rr']}\n")
        f.write(f"  MRR:       {result['mrr']}\n\n")
        if result.get('analysis'):
            f.write(f"AI-анализ:\n{result['analysis']}\n")

    return result


# ===== СКАЧАТЬ ФАЙЛ =====

@download_router.get("/download")
async def download():
    """ Для загрузки результатов проведенного анализа (последнего)"""
    return FileResponse(
        "last_result.txt",
        media_type="text/plain",
        filename="metrics_result.txt"
    )



@health_router.get("/health/ai")
async def health_ai():
    """ Позволяет проверить AI в любой момент после запуска, а не только при старте.

    В отличие от lifespan (который выполняется однократно), этот эндпоинт
    нужен для периодического внешнего контроля — мониторинга, Kubernetes probes.
    Так мы узнаём о проблемах с AI не при следующем перезапуске, а сразу.
    """
    test_metrics = {
        "accuracy": 0.0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
        "rr": 0.0,
        "mrr": 0.0
    }
    try:
        result = await run_in_threadpool(analyze_metrics, test_metrics)
        if result.startswith("Ошибка"):
            return JSONResponse(
                status_code=503,
                content={"ai_status": "error", "detail": result}
            )
        return {"ai_status": "ok"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"ai_status": "error", "detail": str(e)}
        )

app.include_router(download_router)
app.include_router(health_router)

# uvicorn main:app --reload
# uvicorn main:app --reload --port 8001