from flask import Flask, render_template, request, send_file
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remover_silencio', methods=['POST'])
def remover_silencio():
    audio = request.files['audio']
    stop_periods = request.form['stopPeriods']
    stop_duration = request.form['stopDuration']
    stop_threshold = request.form['stopThreshold']

    filename = secure_filename(audio.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, "limpo_" + filename)

    audio.save(input_path)

    cmd = [
        "ffmpeg",
        "-y",  # overwrite
        "-i", input_path,
        "-af",
        f"silenceremove=stop_periods={stop_periods}:stop_duration={stop_duration}:stop_threshold={stop_threshold}dB",
        output_path
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    from os import environ
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
