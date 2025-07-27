from fastapi import FastAPI
from modules.triage_ai.model import triage_predict

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Enterprise AI ED API"}

@app.post("/triage/")
def predict_triage(payload: dict):
    result = triage_predict(**payload)
    return result
