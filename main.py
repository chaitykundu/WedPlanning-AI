import argparse
from services.pdf_reader import extract_text_from_pdf
from services.ai_timeline_generator import WeddingTimelineAI

def main():
    parser = argparse.ArgumentParser(description="AI Wedding Timeline Generator")
    parser.add_argument("--intake", required=True, help="Path to filled Wedding Intake Questionnaire PDF")
    parser.add_argument("--reference", required=True, help="Path to reference Day-of Timeline PDF")
    args = parser.parse_args()

    print("📥 Reading uploaded files...")
    intake_text = extract_text_from_pdf(args.intake)
    reference_text = extract_text_from_pdf(args.reference)

    print("\n🧠 Generating modeled Day-of Timeline...")
    ai = WeddingTimelineAI()
    timeline_output = ai.generate_timeline(intake_text, reference_text)

    print("\n✅ --- AI-GENERATED DAY-OF TIMELINE --- ✅\n")
    print(timeline_output)

if __name__ == "__main__":
    main()
