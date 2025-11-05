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
async def chat(user_message: str = Form(...)):
    """
    Handles chat messages from the user.
    """
    response = bot.chat(user_message)
    return {"reply": response}

@app.post("/upload-file")
async def upload_file(
    files: list[UploadFile] = File(...),
    prompt: str = Form(...),
):
    """
    Handles multiple file uploads and a text prompt.
    """
    file_analysis = await handle_file_upload(files)

    chatbot_response = bot.chat(prompt)
    return {"files": file_analysis, "chatbot_response": chatbot_response}

@app.post("/generate-timeline")
async def generate_timeline(
    prompt: str = Form(...),
    files: list[UploadFile] = File(None),
):
    """
    Generates a wedding day timeline based on uploaded files and/or a text prompt.
    """
    uploaded_file_paths = []
    if files:
        os.makedirs("uploads", exist_ok=True)
        for f in files:
            file_path = os.path.join("uploads", f.filename)
            with open(file_path, "wb") as out:
                content = await f.read()
                out.write(content)
            uploaded_file_paths.append(file_path)

    result = generator.generate_timeline(prompt_text=prompt, uploaded_files=uploaded_file_paths)
    return {"timeline": result}
