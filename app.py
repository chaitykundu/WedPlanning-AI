import streamlit as st
from services.pdf_reader import extract_text_from_pdf
from services.ai_timeline_generator import WeddingTimelineAI
import tempfile
import os

st.set_page_config(page_title="💍 AI Wedding Timeline Generator", layout="centered")

st.title("💍 AI Wedding Timeline Generator")
st.caption("Upload your filled Wedding Intake Questionnaire and a sample reference timeline to generate a modeled day-of timeline.")

# --- File upload widgets ---
intake_file = st.file_uploader("📄 Upload Filled Wedding Intake Questionnaire", type=["pdf"])
reference_file = st.file_uploader("📘 Upload Reference Day-of Timeline", type=["pdf"])

generate_button = st.button("✨ Generate Timeline")

if generate_button:
    if not intake_file or not reference_file:
        st.error("Please upload both the intake and reference PDF files.")
    else:
        with st.spinner("Extracting text from PDFs..."):
            # Save uploaded files temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_intake:
                temp_intake.write(intake_file.read())
                intake_path = temp_intake.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_ref:
                temp_ref.write(reference_file.read())
                reference_path = temp_ref.name

            # Extract text from PDFs
            intake_text = extract_text_from_pdf(intake_path)
            reference_text = extract_text_from_pdf(reference_path)

        st.success("✅ Files processed successfully!")

        # Display extracted preview
        with st.expander("📝 Preview Intake Text"):
            st.text(intake_text[:1500])

        with st.expander("📋 Preview Reference Timeline"):
            st.text(reference_text[:1500])

        # Generate AI-based timeline
        with st.spinner("🧠 Generating your customized Day-of Timeline..."):
            ai = WeddingTimelineAI()
            timeline_output = ai.generate_timeline(intake_text, reference_text)

        st.subheader("🗓️ AI-Generated Day-of Wedding Timeline")
        st.markdown(timeline_output)

        # Offer download option
        output_path = os.path.join("uploads", "AI_Generated_Timeline.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(timeline_output)

        with open(output_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Timeline as Text File",
                data=f,
                file_name="AI_Wedding_Timeline.txt",
                mime="text/plain",
            )
