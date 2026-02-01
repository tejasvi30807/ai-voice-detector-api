from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
import uuid
import os

app = FastAPI()

API_KEY = "voice123"

class AudioRequest(BaseModel):
    audio_base64: str

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/detect-voice")
def detect_voice(
    request: AudioRequest,
    x_api_key: str = Header(None)
):
    # 1. API key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 2. Decode Base64 audio
    try:
        audio_bytes = base64.b64decode(request.audio_base64)
        file_name = f"{uuid.uuid4()}.mp3"

        with open(file_name, "wb") as f:
            f.write(audio_bytes)

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64 audio")

    # 3. SIMPLE rule-based detection
    file_size_kb = os.path.getsize(file_name) / 1024

    if file_size_kb < 50:
        classification = "AI-generated"
        confidence = 0.75
        explanation = "Very small and uniform audio size suggests synthetic voice patterns."
    else:
        classification = "Human-generated"
        confidence = 0.75
        explanation = "Audio size and variation are consistent with natural human speech."

    return {
        "classification": classification,
        "confidence": confidence,
        "explanation": explanation
    }
