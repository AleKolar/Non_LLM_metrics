# src/main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool

from src.schemas.metrics import MetricsInput
from src.services.metrics.ai_service import analyze_metrics
from src.services.metrics.metrics_service import calculate_metrics

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html"
    )


@app.post("/metrics")
async def metrics(payload: MetricsInput):
    result = calculate_metrics(
        tp=payload.get("tp", 0),
        tn=payload.get("tn", 0),
        fp=payload.get("fp", 0),
        fn=payload.get("fn", 0),
        first_relevant_rank=payload.get("first_relevant_rank", 1),
        ranks=payload.get("ranks")
    )

    #result["analysis"] = analyze_metrics(result)
    result["analysis"] = await run_in_threadpool(analyze_metrics, result)

    return result

# uvicorn main:app --reload
