import os
from contextlib import asynccontextmanager
import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from stock_prediction import logger
import uvicorn

model_name = "arima_model"
model_alias = "champion"
mlflow_tracking_uri = "http://127.0.0.1:5000"
model_uri = f"models:/{model_name}@{model_alias}"
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    logger.info(f"Loading model from {model_uri} tracking_uri={mlflow_tracking_uri}")
    try:
     ml_models["arima"] = mlflow.statsmodels.load_model(model_uri)
     logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model at startup: {e}")
        ml_models["arima"] = None
    yield
    ml_models.clear()
app = FastAPI(title="Stock Price Prediction App", lifespan=lifespan)

class PredictRequest(BaseModel):
    steps: int = Field(default=5, ge=1, le=50, description="Number of future days to forecast")
    
class ForecastPoint(BaseModel):
    date: str
    prediction: float

class PredictResponse(BaseModel):
    model_name: str
    model_alias: str
    steps: int
    forecasts: list[ForecastPoint]

@app.get("/health")
def health():
    model_loaded = ml_models.get("arima") is not None
    return {
        "status": "ok" if model_loaded else "model_unavailable",
        "model_uri": model_uri
        
    }
@app.post("/reload_model")
def reload_model():
    try: 
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        ml_models["arima"] = mlflow.statsmodels.load_model(model_uri)
        return {"status": "reloaded", "model_uri": model_uri}
    except Exception as e:
        logger.error(f"Reloading model failed: {e}")
        raise HTTPException(status_code=503, detail=f"Could not reload model: {e}")
    
@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    model = ml_models.get("arima")
    if model is None:
        raise HTTPException(status=503, detail="Model not loaded. Try reloading via /reload_model or check /health")
    try:
        forecasts = model.forecast(steps=request.steps)
    except Exception as e:
        logger.error(f"Forecaste failed: {e}")
        raise HTTPException(status_code=500, detail=f"Forecast Failed: {e}")
    points = []
    for date, value in forecasts.items():
        if isinstance(date, pd.Timestamp):
            label = str(date.date())
        else:
            label = f"step_{date}"
        points.append(ForecastPoint(date=label, prediction=float(value)))
    return PredictResponse(
        model_name=model_name,
        model_alias=model_alias,
        steps=request.steps,
        forecasts = points
    )
        


if __name__ =="__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=80)
    



# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from stock_prediction.constants import CONFIG_FILE_PATH
# from stock_prediction.utils.common import read_yaml, load_bin
# from pathlib import Path
# import os
# import joblib
# import uvicorn

# config = read_yaml(CONFIG_FILE_PATH)
# MODEL_PATH = config.model_evaluation.model_path

# app = FastAPI(title="Stock price prediction App")
# print(app)
# model = None
# @app.on_event("startup")
# def load_model():
#     global model
#     if not os.path.exists(MODEL_PATH):
#         raise RuntimeError(f"Model file not found at {MODEL_PATH}")
#     model = load_bin(Path(MODEL_PATH))
    
# class PredictRequest(BaseModel):
#     steps: int = Field(default=5, ge=1, le=50, description="Number of future days to forecast")

# @app.get("/health")
# def health():
#     return{
#         "status": "ok" if model is not None else "model_unavailable",  "model_path": MODEL_PATH
#     }



# @app.post("/predict")
# def predict(request: PredictRequest):
#     if model is None:
#         raise HTTPException(status_code=503, detail="Model not loaded")
#     try:
#         forecast = model.forecast(steps=request.steps)
#     except Exception as e:
#         raise HTTPException(status_code=503, detail=f"Forecast failed: {e}")
#     return {
#         "steps": request.steps,
#         "forecast": [
#             {"date": (date.date()), "forecast_close": (float(value)) }
#             for date, value in forecast.items()
            
#         ]
#     }
# if __name__ =="__main__":
#     uvicorn.run(app=app, host="0.0.0.0", port=80)
    