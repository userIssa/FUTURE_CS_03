import os
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from encryption import encrypt_file, decrypt_file
import pathlib

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Flask session secret

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file selected")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("Empty filename")
            return redirect(request.url)

        filename = file.filename
        file_data = file.read()
        encrypted = encrypt_file(file_data, filename)

        filepath = os.path.join(UPLOAD_FOLDER, filename + ".enc")
        with open(filepath, "wb") as f:
            f.write(encrypted)

        flash(f"File {filename} uploaded and encrypted successfully!")
        return redirect(url_for("index"))

    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".enc")]
    return render_template("index.html", files=files)

@app.route("/download/<filename>")
def download(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        flash("File not found")
        return redirect(url_for("index"))

    with open(filepath, "rb") as f:
        encrypted = f.read()
    original_name = filename.replace(".enc", "")
    decrypted = decrypt_file(encrypted, original_name)

    output_path = os.path.join(UPLOAD_FOLDER, original_name)
    with open(output_path, "wb") as f:
        f.write(decrypted)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
