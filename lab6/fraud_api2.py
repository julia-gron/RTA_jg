from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
 
app = FastAPI(title="Fraud Detection API")
model = pickle.load(open('fraud_model.pkl', 'rb'))
 
@app.get("/health")
def health():
    return {"status": "ok", "model": "RandomForest", "features": 3}
