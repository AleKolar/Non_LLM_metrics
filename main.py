# src/main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool
from starlette.responses import JSONResponse

from src.schemas.metrics import MetricsInput
from src.services.metrics.ai_service import analyze_metrics
from src.services.metrics.metrics_service import calculate_metrics

templates = Jinja2Templates(directory="src/templates")

from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при старте
    try:
        # Простейшая проверка: вызов AI с минимальными данными
        test_metrics = {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
            "rr": 0.0,
            "mrr": 0.0
        }
        # Запускаем через run_in_threadpool, как и в эндпоинте
        from starlette.concurrency import run_in_threadpool
        result = await run_in_threadpool(analyze_metrics, test_metrics)
        if result.startswith("Ошибка"):
            print(f"⚠️ AI-сервис недоступен: {result}")
        else:
            print("✅ AI-сервис доступен")
    except Exception as e:
        print(f"⚠️ Не удалось проверить AI-сервис: {e}")

    yield  # Работает app

    # Действия при завершении (если нужно)

app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html"
    )


@app.post("/metrics")
async def metrics(payload: MetricsInput):
    result = calculate_metrics(
        tp=payload.tp,
        tn=payload.tn,
        fp=payload.fp,
        fn=payload.fn,
        first_relevant_rank=payload.first_relevant_rank,
        ranks=payload.ranks
    )

    #result["analysis"] = analyze_metrics(result)
    result["analysis"] = await run_in_threadpool(analyze_metrics, result)

    return result

@app.get("/health/ai")
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

# uvicorn main:app --reload
