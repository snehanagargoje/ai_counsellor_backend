from fastapi import FastAPI

app = FastAPI(title="AI Counsellor API")

@app.get("/")
def root():
    return {"status": "AI Counsellor backend running"}
