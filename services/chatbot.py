import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class WeddingPlannerChatbot:
    """
    AI Chatbot for wedding planning assistance using Google Gemini API.
    """

    def __init__(self, model="gemini-2.5-flash"):
        self.model = genai.GenerativeModel(model)
        self.chat_session = self.model.start_chat(history=[])
        self.first_message = True 

    def chat(self, user_message: str) -> str:
        """
        Handles user queries and returns AI responses about wedding planning.
        """
        # Friendly, simple tone for first conversation
        if self.first_message:
            prompt = f"""
            You are a warm, friendly wedding planner chatbot.
            Greet the user casually and kindly.
            Keep the message short and natural (2–3 lines max).
            
            User: {user_message}
            """
            self.first_message = False
        else:
            prompt = f"""
            You are an expert wedding planner chatbot assistant.
            Be friendly, creative, and detail-oriented.

            The user may ask about:
            - Wedding timeline suggestions
            - Venue ideas
            - Budget planning
            - Vendor coordination
            - Decoration themes
            - Guest management
            - Bridal preparation or schedule
            - dietary_restrictions
            - Wrap-Up & Exit

            Always reply naturally, as if chatting with a couple planning their big day.

            User: {user_message}
            """
        response = self.chat_session.send_message(prompt)
        return response.text.strip()
