import os
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from encryption import encrypt_file, decrypt_file

app = Flask(__name__)
app.secret_key = "supersecret"  # needed for flash messages

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("No file selected!")
            return redirect(url_for("index"))

        # Encrypt file data
        file_data = file.read()
        encrypted_data = encrypt_file(file_data)

        save_path = os.path.join(UPLOAD_FOLDER, file.filename + ".enc")
        with open(save_path, "wb") as f:
            f.write(encrypted_data)

        flash(f"File {file.filename} uploaded and encrypted successfully!")
        return redirect(url_for("index"))

    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)

@app.route("/download/encrypted/<filename>")
def download_encrypted(filename):
    """Download the encrypted version of the file"""
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path, as_attachment=True)

@app.route("/download/decrypt/<filename>")
def download_decrypt(filename):
    """Decrypt file on the fly and return original"""
    path = os.path.join(UPLOAD_FOLDER, filename)
    with open(path, "rb") as f:
        encrypted_data = f.read()
    decrypted_data = decrypt_file(encrypted_data)

    # remove `.enc` extension if present
    original_name = filename[:-4] if filename.endswith(".enc") else filename

    # wrap decrypted bytes in BytesIO for Flask
    buffer = BytesIO()
    buffer.write(decrypted_data)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=original_name,
        mimetype="application/octet-stream"
    )

if __name__ == "__main__":
    app.run(debug=True)
