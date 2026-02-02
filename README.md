# AI Voice Detector API

A FastAPI-based API to detect whether a voice is human or AI-generated.

## Base URL
https://ai-voice-detector-api.onrender.com

## Endpoint
POST /detect-voice

## Headers
x-api-key: voice123

## Request Body
```json
{
  "language": "Tamil",
  "audioFormat": "mp3",
  "audio_base64": "base64_encoded_audio"
}
