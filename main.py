import argparse
from services.pdf_reader import extract_text_from_pdf
from services.ai_timeline_generator import WeddingTimelineAI
from services.speech_to_text import transcribe_audio
import os

def main():
    parser = argparse.ArgumentParser(description="AI Wedding Timeline Generator (CLI)")
    parser.add_argument("--intake", required=True, help="Path to filled Wedding Intake Questionnaire PDF")
    parser.add_argument("--reference", required=True, help="Path to reference Day-of Timeline PDF")
    parser.add_argument("--audio", required=False, help="Path to meeting recording (optional)")
    args = parser.parse_args()

    print("📥 Reading uploaded files...")
    intake_text = extract_text_from_pdf(args.intake)
    reference_text = extract_text_from_pdf(args.reference)

    meeting_text = ""
    if args.audio and os.path.exists(args.audio):
        print(f"🎧 Transcribing meeting recording: {args.audio}")
        meeting_text = transcribe_audio(args.audio)

    print("\n🧠 Generating modeled Day-of Timeline...")
    ai = WeddingTimelineAI()
    combined_context = intake_text + "\n\n" + meeting_text
    timeline_output = ai.generate_timeline(combined_context, reference_text)

    print("\n✅ --- AI-GENERATED DAY-OF TIMELINE --- ✅\n")
    print(timeline_output)

if __name__ == "__main__":
    main()
