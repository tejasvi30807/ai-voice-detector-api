from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64

app = FastAPI()

# API Key
API_KEY = "voice123"


# Request body model
class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audio_base64: str


@app.post("/detect-voice")
def detect_voice(
    request: VoiceRequest,
    x_api_key: str = Header(...)
):
    # API key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Decode base64 audio
    try:
        audio_bytes = base64.b64decode(request.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio")

    # Dummy response (for testing)
    return {
        "language": request.language,
        "audio_format": request.audioFormat,
        "prediction": "human",
        "confidence": 0.85
    }
