from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Counsellor API")

@app.get("/")
def root():
    return {"status": "AI Counsellor backend running"}

class CounselRequest(BaseModel):
    message: str

@app.post("/counsel")
def counsel_user(data: CounselRequest):
    return {
        "user_message": data.message,
        "counsellor_reply": "I understand how you feel. I'm here to help you."
    }
