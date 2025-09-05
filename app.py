from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
from encryption import encrypt_file, decrypt_file

app = Flask(__name__)
app.secret_key = "supersecret"  # needed for flash messages

UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = "encrypted"
DECRYPTED_FOLDER = "decrypted"

# Make sure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if file was uploaded
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file:
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Encrypt file
            encrypted_path = os.path.join(ENCRYPTED_FOLDER, filename + ".bin")
            encrypt_file(file_path, encrypted_path)

            flash("File encrypted successfully!")
            return send_file(encrypted_path, as_attachment=True)

    return render_template("index.html")


@app.route("/decrypt", methods=["POST"])
def decrypt():
    if "file" not in request.files:
        flash("No file part")
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("index"))

    if file:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Decrypt file
        decrypted_path = os.path.join(DECRYPTED_FOLDER, filename.replace(".bin", ""))
        try:
            decrypt_file(file_path, decrypted_path)
            flash("File decrypted successfully!")
            return send_file(decrypted_path, as_attachment=True)
        except Exception as e:
            flash(f"Decryption failed: {str(e)}")
            return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
