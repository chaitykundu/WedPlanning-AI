import streamlit as st
from services.pdf_reader import extract_text
from services.ai_timeline_generator import WeddingTimelineAI
from services.speech_to_text import transcribe_audio
import tempfile
import os
import time

# ----------------------------
# Streamlit Setup
# ----------------------------
st.set_page_config(page_title="💍 AI Wedding Planner Assistant", layout="wide")

st.title("💍 AI Wedding Planner Assistant")
st.caption("Your personalized wedding planning assistant. You can chat freely, ask for ideas, or upload documents and recordings for AI-powered planning assistance.")

# ----------------------------
# Initialize Session Memory
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# File Upload Section
# ----------------------------
with st.sidebar:
    st.header("📎 Optional Uploads")
    st.markdown("You can upload any of the following to help me plan better:")
    intake_file = st.file_uploader("📄 Wedding Intake Questionnaire", type=["pdf", "docx"])
    reference_file = st.file_uploader("📘 Sample or Reference Timeline", type=["pdf", "docx"])
    audio_file = st.file_uploader("🎙️ Meeting Recording (optional)", type=["mp3", "wav", "m4a"])

    uploaded_files = []
    if intake_file:
        uploaded_files.append("Intake")
    if reference_file:
        uploaded_files.append("Reference Timeline")
    if audio_file:
        uploaded_files.append("Audio Recording")

    if uploaded_files:
        st.success(f"✅ Uploaded: {', '.join(uploaded_files)}")
    else:
        st.info("No files uploaded yet. You can still chat freely!")

# ----------------------------
# Chat Input
# ----------------------------
user_prompt = st.chat_input("Ask me anything about your wedding planning...")

if user_prompt:
    # Display user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Prepare Assistant response placeholder
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("💭 Thinking...")

        # ----------------------------
        # File Handling (Optional Context)
        # ----------------------------
        intake_text = ""
        reference_text = ""
        meeting_text = ""

        # Process intake or reference docs if uploaded
        if intake_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(intake_file.name)[1]) as temp_intake:
                temp_intake.write(intake_file.read())
                intake_path = temp_intake.name
            intake_text = extract_text(intake_path)

        if reference_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(reference_file.name)[1]) as temp_ref:
                temp_ref.write(reference_file.read())
                reference_path = temp_ref.name
            reference_text = extract_text(reference_path)

        # Transcribe meeting audio if uploaded
        if audio_file:
            message_placeholder.markdown("🎧 Transcribing meeting recording...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_file.read())
                audio_path = temp_audio.name
            meeting_text = transcribe_audio(audio_path)

        # ----------------------------
        # Combine context and prompt
        # ----------------------------
        full_context = ""
        if intake_text or reference_text or meeting_text:
            full_context += "Here are the user's provided files and meeting notes:\n"
            if intake_text:
                full_context += f"\n--- Intake Questionnaire ---\n{intake_text}\n"
            if reference_text:
                full_context += f"\n--- Reference Timeline ---\n{reference_text}\n"
            if meeting_text:
                full_context += f"\n--- Meeting Notes ---\n{meeting_text}\n"
            full_context += "\nNow respond to the following user query considering these materials:\n"
        full_context += user_prompt

        # ----------------------------
        # Generate AI Response
        # ----------------------------
        ai = WeddingTimelineAI()
        response = ai.generate_timeline(full_context, reference_text or "")

        # Simulate typing effect
        final_response = ""
        for word in response.split():
            final_response += word + " "
            message_placeholder.markdown(final_response + "▌")
            time.sleep(0.015)
        message_placeholder.markdown(final_response.strip())

        # Save in session
        st.session_state.messages.append({"role": "assistant", "content": final_response.strip()})
