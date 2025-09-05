import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from encryption import encrypt_file, decrypt_file
from werkzeug.utils import secure_filename

# Flask setup
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

# File upload directories
UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = os.path.join(UPLOAD_FOLDER, "encrypted")
DECRYPTED_FOLDER = os.path.join(UPLOAD_FOLDER, "decrypted")

# Ensure folders exist
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part in request.")
            return redirect(url_for("index"))

        file = request.files["file"]
        if file.filename == "":
            flash("No file selected.")
            return redirect(url_for("index"))

        filename = secure_filename(file.filename)
        file_path = os.path.join(ENCRYPTED_FOLDER, filename)

        # Save uploaded file temporarily
        file.save(file_path)

        # Encrypt it
        encrypted_path = file_path + ".bin"
        encrypt_file(file_path, encrypted_path)

        # Remove original uploaded file (optional)
        os.remove(file_path)

        flash("File encrypted successfully!")
        return send_file(encrypted_path, as_attachment=True)

    return render_template("index.html")


@app.route("/decrypt", methods=["POST"])
def decrypt():
    if "file" not in request.files:
        flash("No file part in request.")
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    file_path = os.path.join(DECRYPTED_FOLDER, filename)

    # Save encrypted file temporarily
    file.save(file_path)

    # Decrypt it
    decrypted_path = os.path.join(
        DECRYPTED_FOLDER, filename.replace(".bin", "_decrypted.txt")
    )
    try:
        decrypt_file(file_path, decrypted_path)
        flash("File decrypted successfully!")
        return send_file(decrypted_path, as_attachment=True)
    except Exception as e:
        flash(f"Decryption failed: {str(e)}")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
