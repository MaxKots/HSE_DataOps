import json
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.model import predict, MODEL_VERSION
from app.schemas import PredictRequest, PredictResponse
from app.database import init_db, log_prediction

logging.basicConfig(
    format='{"time":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    logger.info("DB initialized, model loaded")
    yield


app = FastAPI(title="ML Service", version=MODEL_VERSION, lifespan=lifespan)
Instrumentator().instrument(app).expose(app)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    return {"status": "ready"}


@app.post("/api/v1/predict", response_model=PredictResponse)
def api_predict(req: PredictRequest):
    start = time.time()
    result = predict(req.features)
    elapsed = time.time() - start

    log_prediction(
        input_data=json.dumps(req.features),
        output=result,
        model_version=MODEL_VERSION,
    )

    logger.info(
        f"prediction input={req.features} output={result:.4f} "
        f"time={elapsed:.4f}s version={MODEL_VERSION}"
    )

    return PredictResponse(prediction=result, model_version=MODEL_VERSION)