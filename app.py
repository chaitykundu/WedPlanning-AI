import streamlit as st
from services.pdf_reader import extract_text_from_pdf
from services.ai_timeline_generator import WeddingTimelineAI
from services.speech_to_text import transcribe_audio
import tempfile
import os
import time

# ----------------------------
# Streamlit Chat-Like Setup
# ----------------------------
st.set_page_config(page_title="💍 AI Wedding Planner", layout="wide")

st.title("💍 AI Wedding Planner Assistant")
st.caption("Upload your intake questionnaire, reference timeline, and optional meeting recording — the AI will generate a structured 'Day-of Wedding Timeline' just like a professional planner.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# File Uploads
# ----------------------------
with st.sidebar:
    st.header("📁 Upload Your Files")
    intake_file = st.file_uploader("📄 Intake Questionnaire", type=["pdf"])
    reference_file = st.file_uploader("📘 Reference Timeline", type=["pdf"])
    audio_file = st.file_uploader("🎙️ Meeting Recording (optional)", type=["mp3", "wav", "m4a"])

    if intake_file and reference_file:
        st.success("✅ Files ready to process!")
    else:
        st.info("Please upload at least intake & reference PDFs.")

# ----------------------------
# Chat Input
# ----------------------------
user_prompt = st.chat_input("Ask the AI to generate or adjust your wedding timeline...")

if user_prompt:
    # Display user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Check required uploads
    if not intake_file or not reference_file:
        ai_reply = "⚠️ Please upload both the intake and reference PDF files first."
        with st.chat_message("assistant"):
            st.markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    else:
        # ---------------------------------
        # File handling & AI generation
        # ---------------------------------
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🧠 Reading your files...")

            # Save temporary copies
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_intake:
                temp_intake.write(intake_file.read())
                intake_path = temp_intake.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_ref:
                temp_ref.write(reference_file.read())
                reference_path = temp_ref.name

            # Extract text
            intake_text = extract_text_from_pdf(intake_path)
            reference_text = extract_text_from_pdf(reference_path)

            # Transcribe meeting audio if provided
            meeting_text = ""
            if audio_file:
                message_placeholder.markdown("🎧 Transcribing meeting recording...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                    temp_audio.write(audio_file.read())
                    audio_path = temp_audio.name
                meeting_text = transcribe_audio(audio_path)

            # Generate AI timeline
            message_placeholder.markdown("✨ Generating your wedding day timeline...")
            ai = WeddingTimelineAI()
            combined_input = intake_text + "\n\n" + meeting_text + "\n\n" + user_prompt
            timeline_output = ai.generate_timeline(combined_input, reference_text)

            # Simulate streaming / typing
            final_response = ""
            for chunk in timeline_output.split():
                final_response += chunk + " "
                message_placeholder.markdown(final_response + "▌")
                time.sleep(0.02)
            message_placeholder.markdown(final_response)

            # Store in chat history
            st.session_state.messages.append({"role": "assistant", "content": final_response})
