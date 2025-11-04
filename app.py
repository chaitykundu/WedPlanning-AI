import os
import uuid
import traceback
from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify, flash
from werkzeug.utils import secure_filename
from services.pdf_reader import extract_text
from services.ai_timeline_generator import WeddingTimelineAI

# --- Config ---
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "csv"}
MAX_CONTENT_LENGTH = 40 * 1024 * 1024  # 40 MB per request

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")  # replace in prod

# Default internal reference template (used instead of separate reference file)
DEFAULT_REFERENCE_TEXT = """
Day-of Timeline Template
- Header: Couple names, wedding date, venue(s)
- Contact block: Main contact + vendor phone numbers
- Timeline: Absolute times with short descriptions (prep, travel, ceremony, photos, cocktail, reception, first dance, toasts, cake, send-off)
- Notes: Vendor load-in, parking, backup plan, timeline buffers
Tone: concise, production-ready for vendors.
"""

# --- Helpers ---
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file_storage):
    """Save uploaded FileStorage to uploads/ with a unique name and return saved path."""
    filename = secure_filename(file_storage.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
    file_storage.save(path)
    return path

def cleanup_paths(*paths):
    for p in paths:
        try:
            if p and os.path.exists(p):
                os.remove(p)
        except Exception:
            app.logger.exception("Failed to cleanup %s", p)

# --- Routes ---
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    """
    Web form POST handler:
    - Expects one or more files under the field name 'files' (multipart form).
    - Combines extracted text from all files and generates a single timeline.
    """
    files = request.files.getlist("files")
    if not files or all(f.filename == "" for f in files):
        flash("Please add at least one file.", "danger")
        return redirect(url_for("index"))

    # Validate file types
    for f in files:
        if not allowed_file(f.filename):
            flash(f"File not allowed: {f.filename}. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}", "danger")
            return redirect(url_for("index"))

    saved_paths = []
    try:
        # Save uploads and extract text from each
        texts = []
        original_names = []
        for f in files:
            saved = save_uploaded_file(f)
            saved_paths.append(saved)
            original_names.append(f.filename)
            extracted = extract_text(saved)
            texts.append(extracted or "")

        # Combine all extracted text into one context
        combined_context = "\n\n".join(texts).strip()
        if not combined_context:
            flash("No text could be extracted from uploaded files.", "danger")
            return redirect(url_for("index"))

        # Use default reference template (no separate reference)
        reference_text = DEFAULT_REFERENCE_TEXT

        ai = WeddingTimelineAI()
        timeline_output = ai.generate_timeline(combined_context, reference_text)

        # Save generated timeline
        out_filename = f"timeline_{uuid.uuid4().hex}.txt"
        output_path = os.path.join(app.config["UPLOAD_FOLDER"], out_filename)
        with open(output_path, "w", encoding="utf-8") as f_out:
            f_out.write(timeline_output.strip())

        # Render result
        return render_template("result.html",
                               timeline=timeline_output,
                               download_url=url_for("download", filename=out_filename),
                               uploaded_names=original_names)
    except Exception as e:
        app.logger.error("Error generating timeline: %s\n%s", str(e), traceback.format_exc())
        flash(f"An error occurred while generating timeline: {str(e)}", "danger")
        return redirect(url_for("index"))
    finally:
        # cleanup uploaded source files (keep generated output)
        cleanup_paths(*saved_paths)

@app.route("/api/generate", methods=["POST"])
def api_generate():
    """
    Programmatic endpoint:
    - Accepts multipart/form-data with one or more files (field name 'files').
    - Returns JSON: { "timeline": "...", "download": "/download/..." }
    """
    files = request.files.getlist("files")
    if not files or all(f.filename == "" for f in files):
        return jsonify({"error": "At least one file must be uploaded under 'files'."}), 400

    for f in files:
        if not allowed_file(f.filename):
            return jsonify({"error": f"File not allowed: {f.filename}"}), 400

    saved_paths = []
    try:
        texts = []
        for f in files:
            saved = save_uploaded_file(f)
            saved_paths.append(saved)
            texts.append(extract_text(saved) or "")

        combined_context = "\n\n".join(texts).strip()
        if not combined_context:
            return jsonify({"error": "No extractable text found in uploaded files."}), 400

        reference_text = DEFAULT_REFERENCE_TEXT
        ai = WeddingTimelineAI()
        timeline_output = ai.generate_timeline(combined_context, reference_text)

        out_filename = f"timeline_{uuid.uuid4().hex}.txt"
        output_path = os.path.join(app.config["UPLOAD_FOLDER"], out_filename)
        with open(output_path, "w", encoding="utf-8") as f_out:
            f_out.write(timeline_output.strip())

        download_url = url_for("download", filename=out_filename, _external=True)
        return jsonify({"timeline": timeline_output, "download": download_url})
    except Exception as e:
        app.logger.exception("API error")
        return jsonify({"error": str(e)}), 500
    finally:
        cleanup_paths(*saved_paths)

@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    safe_name = secure_filename(filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
    if not os.path.exists(path):
        return "File not found", 404
    return send_file(path, as_attachment=True, download_name=safe_name)

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
