import argparse
from services.pdf_reader import extract_text
from services.ai_timeline_generator import WeddingTimelineAI
import os

def main():
    parser = argparse.ArgumentParser(description="AI Wedding Timeline Generator ")
    parser.add_argument("--intake", required=True, help="Path to filled Wedding Intake Questionnaire PDF")
    parser.add_argument("--reference", required=True, help="Path to reference Day-of Timeline PDF")
    args = parser.parse_args()

    print("📥 Reading uploaded files...")

    # --- Extract text from both PDFs ---
    intake_text = extract_text(args.intake)
    reference_text = extract_text(args.reference)

    # --- Combine context (no audio for now) ---
    combined_context = intake_text  # meeting_text removed

    print("\n🧠 Generating modeled Day-of Timeline...")
    ai = WeddingTimelineAI()
    timeline_output = ai.generate_timeline(combined_context, reference_text)

    print("\n✅ --- AI-GENERATED DAY-OF TIMELINE --- ✅\n")
    print(timeline_output)

if __name__ == "__main__":
    main()
