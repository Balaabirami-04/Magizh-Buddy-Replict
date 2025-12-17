from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="AI Companion API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
os.makedirs("static/audio", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    text: str
    user_id: str = "default_user"


@app.get("/")
async def root():
    return {"message": "AI Companion API is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# -----------------------------
# TEXT CHAT ENDPOINT
# -----------------------------
@app.post("/chat/text")
async def chat_text(request: ChatRequest):
    try:
        ai_res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are MagizhBuddy, a friendly emotional companion."},
                {"role": "user", "content": request.text}
            ]
        )

        reply = ai_res.choices[0].message["content"]

        return {
            "response": reply,
            "emotion": "positive"
        }

    except Exception as e:
        return {
            "response": "I am listening but my brain is not connected to drive. Check API key.",
            "error": str(e)
        }


# -----------------------------
# AUDIO CHAT ENDPOINT
# -----------------------------
@app.post("/chat/audio")
async def chat_audio(file: UploadFile = File(...), user_id: str = Form("default_user")):
    try:
        from voice_service import voice_service

        # Save temp audio file
        temp_filename = f"temp_{file.filename}"
        with open(temp_filename, "wb") as buffer:
            buffer.write(await file.read())

        # Speech to text
        text = await voice_service.speech_to_text(temp_filename)

        os.remove(temp_filename)

        # AI Response
        ai_res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are MagizhBuddy, a fun emotional companion."},
                {"role": "user", "content": text}
            ]
        )

        reply = ai_res.choices[0].message["content"]

        # Convert AI reply to audio
        audio_path = await voice_service.text_to_speech(reply)

        return {
            "text": text,
            "response": reply,
            "emotion": "happy",
            "audio_url": f"/static/audio/{os.path.basename(audio_path)}"
        }

    except Exception as e:
        return {
            "response": "I am listening but my brain is not connected to drive. Check API key.",
            "error": str(e)
        }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
