from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

# -----------------------------
# APP CONFIG
# -----------------------------
app = FastAPI(
    title="AI Career Counsellor",
    description="Emotion + Interest based AI Counsellor",
    version="1.0"
)

# -----------------------------
# CORS CONFIG
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# REQUEST / RESPONSE SCHEMAS
# -----------------------------
class ChatRequest(BaseModel):
    message: str
    language: str = "en"

class ChatResponse(BaseModel):
    reply: str
    emotion: str
    career_interest: str
    current_stage: str
    next_stage: str
    reasoning: List[str]
    universities: List[Dict]

# -----------------------------
# EMOTION DETECTION
# -----------------------------
def detect_emotion(message: str):
    msg = message.lower()

    if any(w in msg for w in ["stress", "stressed", "anxious", "panic", "worried", "pressure"]):
        return "STRESSED"
    if any(w in msg for w in ["confused", "not sure", "uncertain", "lost"]):
        return "CONFUSED"
    if any(w in msg for w in ["ambitious", "top", "best", "ivy", "elite"]):
        return "AMBITION"
    if any(w in msg for w in ["confident", "ready", "sure"]):
        return "CONFIDENT"

    return "NEUTRAL"

# -----------------------------
# CAREER INTEREST DETECTION
# -----------------------------
def detect_career_interest(message: str):
    msg = message.lower()

    if any(w in msg for w in ["engineering", "engineer", "software", "developer", "technology", "computer"]):
        return "ENGINEERING"

    if any(w in msg for w in ["doctor", "medical", "medicine", "mbbs", "healthcare"]):
        return "MEDICAL"

    if any(w in msg for w in ["mba", "management", "business", "entrepreneur"]):
        return "MANAGEMENT"

    if any(w in msg for w in ["politics", "political", "public policy", "government", "civil services"]):
        return "POLITICAL"

    if any(w in msg for w in ["artist", "art", "design", "painting", "fine arts"]):
        return "ARTS"

    if any(w in msg for w in ["music", "musician", "singing", "composer"]):
        return "MUSIC"

    if any(w in msg for w in ["dance", "dancer", "choreography"]):
        return "DANCE"

    if any(w in msg for w in ["law", "lawyer", "legal", "llb"]):
        return "LAW"

    return "GENERAL"

# -----------------------------
# STAGE DECISION
# -----------------------------
def decide_stage(message: str):
    msg = message.lower()

    if "lock" in msg:
        return "LOCKING"
    if "application" in msg or "documents" in msg:
        return "APPLICATION"

    return "DISCOVERY"

# -----------------------------
# UNIVERSITY DATABASE
# -----------------------------
UNIVERSITY_DB = {
    "ENGINEERING": [
        {"name": "TU Munich", "country": "Germany", "risk": "High", "cost": "Medium"},
        {"name": "RWTH Aachen", "country": "Germany", "risk": "Medium", "cost": "Low"},
        {"name": "TU Berlin", "country": "Germany", "risk": "Medium", "cost": "Low"},
        {"name": "University of Toronto", "country": "Canada", "risk": "High", "cost": "High"},
        {"name": "University of Waterloo", "country": "Canada", "risk": "Medium", "cost": "High"},
    ],
    "MEDICAL": [
        {"name": "Heidelberg University", "country": "Germany", "risk": "High", "cost": "Low"},
        {"name": "Charité Berlin", "country": "Germany", "risk": "High", "cost": "Low"},
        {"name": "University of Milan", "country": "Italy", "risk": "Medium", "cost": "Medium"},
    ],
    "MANAGEMENT": [
        {"name": "INSEAD", "country": "France", "risk": "High", "cost": "High"},
        {"name": "ESMT Berlin", "country": "Germany", "risk": "Medium", "cost": "Medium"},
        {"name": "University of Mannheim", "country": "Germany", "risk": "Medium", "cost": "Low"},
    ],
    "POLITICAL": [
        {"name": "Sciences Po", "country": "France", "risk": "High", "cost": "Medium"},
        {"name": "LSE", "country": "UK", "risk": "High", "cost": "High"},
        {"name": "Hertie School", "country": "Germany", "risk": "Medium", "cost": "Medium"},
    ],
    "ARTS": [
        {"name": "University of the Arts London", "country": "UK", "risk": "High", "cost": "High"},
        {"name": "Parsons School of Design", "country": "USA", "risk": "High", "cost": "High"},
        {"name": "Berlin University of the Arts", "country": "Germany", "risk": "Medium", "cost": "Low"},
    ],
    "MUSIC": [
        {"name": "Berklee College of Music", "country": "USA", "risk": "High", "cost": "High"},
        {"name": "Royal College of Music", "country": "UK", "risk": "High", "cost": "High"},
        {"name": "Hanns Eisler School of Music", "country": "Germany", "risk": "Medium", "cost": "Low"},
    ],
    "DANCE": [
        {"name": "Juilliard School", "country": "USA", "risk": "High", "cost": "High"},
        {"name": "London Contemporary Dance School", "country": "UK", "risk": "High", "cost": "High"},
        {"name": "Folkwang University", "country": "Germany", "risk": "Medium", "cost": "Low"},
    ],
    "LAW": [
        {"name": "Harvard Law School", "country": "USA", "risk": "High", "cost": "High"},
        {"name": "Oxford University", "country": "UK", "risk": "High", "cost": "High"},
        {"name": "LMU Munich", "country": "Germany", "risk": "Medium", "cost": "Low"},
    ],
}

# -----------------------------
# UNIVERSITY SELECTION LOGIC
# -----------------------------
def suggest_universities(career, emotion):
    universities = UNIVERSITY_DB.get(career, [])

    if emotion == "STRESSED":
        return universities[-3:]

    if emotion == "AMBITION":
        return universities[:3]

    return universities[:3]

# -----------------------------
# MAIN CHAT API
# -----------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    emotion = detect_emotion(req.message)
    career = detect_career_interest(req.message)
    current_stage = decide_stage(req.message)
    universities = suggest_universities(career, emotion)

    reasoning = [
        f"Detected emotion: {emotion}",
        f"Detected career interest: {career}",
        "Universities selected using emotion + interest logic"
    ]

    reply = (
        f"I understand you are feeling {emotion.lower()}. "
        f"Based on your interest in {career.lower()}, "
        f"I have shortlisted universities suitable for you."
    )

    next_stage = "LOCKING" if current_stage == "DISCOVERY" else "APPLICATION"

    return {
        "reply": reply,
        "emotion": emotion,
        "career_interest": career,
        "current_stage": current_stage,
        "next_stage": next_stage,
        "reasoning": reasoning,
        "universities": universities
    }

# -----------------------------
# FRONTEND COMPATIBILITY API
# -----------------------------
@app.post("/career-advice")
def career_advice(req: ChatRequest):
    return chat(req)
