from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import os
import tempfile
from pydub import AudioSegment
from soda_analysis import perform_soda_analysis
from txt2ipa.kannada2ipa.ipaconvert import ipa2kannada_value

# ✅ Use environment variable for ffmpeg path
FFMPEG_PATH = os.environ.get('FFMPEG_PATH', r"C:\ffmpeg\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe")
AudioSegment.converter = FFMPEG_PATH

app = Flask(__name__)
CORS(app)  # 👈 enables cross-origin requests

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "OK",
        "service": "Flask SODA Analysis Backend",
        "version": "1.0"
    })


@app.route("/analyze_soda", methods=["POST"])
def analyze_soda():
    try:
        target_word = request.form.get("target_word")
        audio_file = request.files.get("audio")

        if not target_word or not audio_file:
            print("🚨 Missing fields:", target_word, audio_file)
            return jsonify({"error": "Missing target word or audio file"}), 400

        unique_id = str(uuid.uuid4())
        temp_path = os.path.join(UPLOAD_FOLDER, f"temp_audio_{unique_id}")
        wav_path = os.path.join(UPLOAD_FOLDER, f"recording_{unique_id}.wav")
        audio_file.save(temp_path)

        sound = AudioSegment.from_file(temp_path)
        sound.export(wav_path, format="wav")
        os.remove(temp_path)

        result = perform_soda_analysis(target_word, wav_path)
        print("✅ SODA Result:", result)
        os.remove(wav_path)  # Clean up processed file

        return jsonify(result)
      
    except Exception as e:
        print("💥 Exception:", e)
        return jsonify({"error": f"Audio processing failed: {str(e)}"}), 400


@app.route("/ipa2kannada", methods=["POST"])
def ipa2kannada_api():
    """
    Convert a list of IPA syllable strings into a single Kannada word.

    Expects JSON:
      { "syllables": ["ipa1", "ipa2", ...] }
    Returns:
      { "word": "<kannada_word>" }
    """
    data = request.get_json(silent=True) or {}
    syllables = data.get("syllables", [])

    if not isinstance(syllables, list):
        return jsonify({"error": "syllables must be a list"}), 400

    try:
        kannada_word = "".join(ipa2kannada_value(s) for s in syllables)
        return jsonify({"word": kannada_word})
    except Exception as e:
        print("💥 ipa2kannada error:", e)
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 400

# ✅ This block must exist at the end to actually run Flask
if __name__ == "__main__":
    # Use PYTHON_PORT to avoid conflict with Node.js PORT
    port = int(os.environ.get("PYTHON_PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"🚀 Starting Flask server on http://0.0.0.0:{port}")
    print(f"🐛 Debug mode: {debug_mode}")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"🎬 FFmpeg path: {FFMPEG_PATH}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)




# # app.py
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from soda_analysis import perform_soda_analysis


# app = Flask(__name__)
# CORS(app)
# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route("/analyze_soda", methods=["POST"])
# def analyze_soda_api():
#     target_word = request.form.get("target_word")
#     audio_file = request.files.get("audio")

#     if not target_word or not audio_file:
#         return jsonify({"error": "Missing target word or audio file"}), 400

#     audio_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
#     audio_file.save(audio_path)

#     try:
#         # result = perform_soda_analysis(target_word, audio_path)
#         output_path = os.path.join("results", f"{target_word}_analysis.json")
#         os.makedirs("results", exist_ok=True)
#         result = perform_soda_analysis(target_word, audio_path, output_path)

#         return jsonify(result)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from pydub import AudioSegment
# from soda_analysis import perform_soda_analysis

# AudioSegment.converter = r"C:\ffmpeg\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route("/analyze_soda", methods=["POST"])
# def analyze_soda():
#     try:
#         target_word = request.form.get("target_word")
#         audio_file = request.files.get("audio")

#         if not target_word or not audio_file:
#             return jsonify({"error": "Missing target word or audio"}), 400

#         temp_path = os.path.join(UPLOAD_FOLDER, "temp")
#         audio_file.save(temp_path)

#         wav_path = os.path.join(UPLOAD_FOLDER, "recording.wav")
#         AudioSegment.from_file(temp_path).export(wav_path, format="wav")
#         os.remove(temp_path)

#         # os.makedirs("results", exist_ok=True)
#         # output_path = f"results/{target_word}_analysis.json"

#         result = perform_soda_analysis(target_word, wav_path)
#         return jsonify(result)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
