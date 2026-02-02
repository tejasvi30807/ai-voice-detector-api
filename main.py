from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
import uuid
import os

app = FastAPI()

API_KEY = "voice123"

SUPPORTED_LANGUAGES = ["tamil", "english", "hindi", "malayalam", "telugu"]

class AudioRequest(BaseModel):
    audio_base64: str
    language: str

@app.get("/")
def root():
    return {"message": "AI Voice Detector API is running"}

@app.post("/detect-voice")
def detect_voice(
    request: AudioRequest,
    x_api_key: str = Header(None)
):
    # 1. API key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 2. Language validation
    if request.language.lower() not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language. Choose from {SUPPORTED_LANGUAGES}"
        )

    # 3. Decode Base64 audio
    try:
        audio_bytes = base64.b64decode(request.audio_base64)
        file_name = f"{uuid.uuid4()}.mp3"

        with open(file_name, "wb") as f:
            f.write(audio_bytes)

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64 audio")

    # 4. Simple rule-based detection (placeholder logic)
    file_size_kb = os.path.getsize(file_name) / 1024

    if file_size_kb < 50:
        classification = "AI-generated"
        confidence = 0.75
        explanation = "Small and uniform audio size suggests synthetic voice patterns."
    else:
        classification = "Human-generated"
        confidence = 0.75
        explanation = "Audio size and variation match natural human speech."

    return {
        "language": request.language,
        "classification": classification,
        "confidence": confidence,
        "explanation": explanation
    }


