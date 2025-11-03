import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class WeddingTimelineAI:
    def __init__(self, model="gemini-2.5-flash"):
        self.model = genai.GenerativeModel(model)

    def generate_timeline(self, intake_text: str, reference_timeline: str) -> str:
        """
        Generates a day-of timeline modeled after the example timeline
        using intake data from the questionnaire.
        """
        prompt = f"""
        You are a professional wedding planner AI assistant.

        Below is a filled-out Wedding Intake Questionnaire containing details for an upcoming wedding:
        ---
        {intake_text}
        ---

        Below is an example reference event timeline to model the structure, tone, and formatting:
        ---
        {reference_timeline}
        ---

        Based on both, create a detailed 'Day-of Wedding Timeline' for this event.
        - Include times, activities, and brief notes (like the reference example).
        - Ensure the timeline logically follows the intake parameters (hair/makeup, ceremony, dinner, etc.).
        - Use clear, consistent formatting with headers and bullet points or a table.

        Output should look like a polished professional wedding planner schedule.
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()
