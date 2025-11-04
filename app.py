from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from services.chatbot import WeddingPlannerChatbot

app = FastAPI(title="Wedding Planner AI 💍")

# Allow frontend access (React, Streamlit, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = WeddingPlannerChatbot()

@app.get("/")
def home():
    return {"message": "Welcome to the Wedding Planner AI API"}

@app.post("/chat")
async def chat(user_message: str = Form(...)):
    """
    Handles chat messages from the user.
    """
    response = bot.chat(user_message)
    return {"reply": response}

@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """
    Handles file uploads (text or PDF).
    """
    contents = await file.read()

    # Convert bytes to text if possible
    try:
        text = contents.decode("utf-8")
    except UnicodeDecodeError:
        return {"error": "Only text-based files are supported for now."}

    result = bot.analyze_file(text, file.filename)
    return {"filename": file.filename, "analysis": result}
