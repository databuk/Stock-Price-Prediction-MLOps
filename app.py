from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from stock_prediction.constants import CONFIG_FILE_PATH
from stock_prediction.utils.common import read_yaml, load_bin
from pathlib import Path
import os
import joblib
import uvicorn

config = read_yaml(CONFIG_FILE_PATH)
MODEL_PATH = config.model_evaluation.model_path

app = FastAPI(title="Stock price prediction App")
print(app)
model = None
@app.on_event("startup")
def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model file not found at {MODEL_PATH}")
    model = load_bin(Path(MODEL_PATH))
    
class PredictRequest(BaseModel):
    steps: int = Field(default=5, ge=1, le=50, description="Number of future days to forecast")

@app.get("/health")
def health():
    return{
        "status": "ok" if model is not None else "model_unavailable",  "model_path": MODEL_PATH
    }



@app.post("/predict")
def predict(request: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        forecast = model.forecast(steps=request.steps)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Forecast failed: {e}")
    return {
        "steps": request.steps,
        "forecast": [
            {"date": (date.date()), "forecast_close": (float(value)) }
            for date, value in forecast.items()
            
        ]
    }
if __name__ =="__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=80)
    
# @app.post("/predict")
# def predict(request: PredictRequest):
#     if model is None:
#         raise HTTPException(status_code=503, detail="Model not loaded")

#     try:
#         forecast = model.forecast(steps=request.steps)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Forecast failed: {e}")

#     return {
#         "steps": request.steps,
#         "forecast": [
#             {"date": str(date.date()), "predicted_close": float(value)}
#             for date, value in forecast.items()
#         ],
#     }