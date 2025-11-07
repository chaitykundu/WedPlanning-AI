import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from services.chatbot import WeddingPlannerChatbot
from services.ai_timeline_generator import WeddingTimelineGenerator
from services.file import handle_file_upload  # Use file upload and extraction logic

app = FastAPI(title="Wedding Planner AI 💍")

# Allow frontend access (React, Streamlit, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL(s) if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = WeddingPlannerChatbot()
generator = WeddingTimelineGenerator()

@app.get("/")
def home():
    return {"message": "Welcome to the Wedding Planner AI Service! "}

@app.post("/chat")
async def chat(
    user_message: str = Form(None),
    file: UploadFile = File(None)
):
    """
    Handles both text messages and file uploads within the chat.
    - If user sends text → normal chat reply.
    - If user uploads files → analyze all files and return instantly.
    - If both → combine file insights + user question.
    """
    if file:
        # Save uploaded file
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", file.filename)
        content = await file.read()
        text_content = content.decode("utf-8", errors="ignore")

        # Analyze the file
        analysis = bot.analyze_file(text_content, file.filename)

        # Optionally, also respond to message if both exist
        if user_message:
            chat_reply = bot.chat(user_message)
            return {
                "reply": chat_reply,
                "file_analysis": analysis,
                "filename": file.filename
            }

        return {
            "reply": analysis,
            "filename": file.filename
        }

    elif user_message:
        response = bot.chat(user_message)
        return {"reply": response}

    else:
        return {"error": "Please provide a message or upload a file."}
