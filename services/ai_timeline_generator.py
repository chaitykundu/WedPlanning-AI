import google.generativeai as genai
import os
from dotenv import load_dotenv
from services.pdf_reader import extract_text

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class WeddingTimelineGenerator:
    """
    Generates a professional 'Day-of Wedding Timeline' based on either:
    - uploaded wedding planning documents, or
    - a written prompt provided by the user.
    """

    def __init__(self, model="gemini-2.5-flash"):
        self.model = genai.GenerativeModel(model)

    def generate_timeline(self, prompt_text: str, uploaded_files: list[str] | None = None) -> str:
        """
        Generates a timeline using uploaded files or user prompt.

        Args:
            prompt_text (str): The user's prompt or wedding instructions.
            uploaded_files (list[str], optional): Paths to uploaded files (PDF, DOCX, CSV, TXT).

        Returns:
            str: AI-generated wedding day timeline.
        """

        # --- Step 1: Build the input context ---
        file_context = ""
        if uploaded_files:
            for path in uploaded_files:
                try:
                    extracted = extract_text(path)
                    file_context += f"\n\n### Content from {os.path.basename(path)} ###\n{extracted}"
                except Exception as e:
                    file_context += f"\n\n[Error reading {path}: {e}]"

        # If files exist, combine both
        if file_context.strip():
            context = f"""
            The following wedding planning information was extracted from the user's uploaded documents:
            ---
            {file_context}
            ---
            Additionally, the user provided this instruction:
            "{prompt_text}"
            """
        else:
            # No files, only use prompt
            context = f"""
            The user provided the following wedding planning instructions:
            ---
            {prompt_text}
            ---
            """

        # --- Step 2: Create prompt for Gemini ---
        prompt = f"""
        You are a highly skilled professional wedding planner AI assistant.

        {context}

        Your task:
        - Create a detailed, realistic, and professional 'Day-of Wedding Timeline.'
        - Organize the day chronologically (morning → ceremony → reception → evening).
        - Include preparation activities, photos, ceremony, cocktail hour, dinner, speeches, and after-party.
        - Use elegant markdown formatting (bold times, section headers, emojis if appropriate).
        - Keep it warm, friendly, and concise, like something a real planner would hand to a client.
        - If details are missing, use reasonable assumptions.
        Example Output Format:
        ---
        **Wedding Day Timeline**

        **7:00 AM – Hair & Makeup**
        - Bride and bridesmaids begin getting ready
        - Photographer arrives for detail shots

        **10:30 AM – Groom Prep**
        - Groomsmen dressing and candid photos

        **4:00 PM – Ceremony**
        - Processional and vows
        - Recessional and couple exit
        ---

        Please generate the best possible wedding day schedule below:
        """

        # --- Step 3: Generate response ---
        response = self.model.generate_content(prompt)
        return response.text.strip()
