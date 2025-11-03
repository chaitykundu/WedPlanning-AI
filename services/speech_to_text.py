import whisper
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL = whisper.load_model("base", device=DEVICE)

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes meeting audio recordings using Whisper base model.
    Returns clean text transcript.
    """
    print(f"[INFO] Transcribing audio from {file_path} using Whisper ({DEVICE})...")
    result = MODEL.transcribe(file_path, fp16=(DEVICE == "cuda"))
    return result.get("text", "").strip()
