from flask import Flask, request, jsonify
import os

app = Flask(__name__)

APP_MESSAGE = os.getenv("APP_MESSAGE", "Hello")
UPLOAD_ALLOWED_EXT = os.getenv("UPLOAD_ALLOWED_EXT", ".txt")
UPLOAD_PASSWORD = os.getenv("UPLOAD_PASSWORD", "secret")

DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.route("/", methods=["GET"])
def list_files():
    files = os.listdir(DATA_DIR)
    return jsonify(files)

@app.route("/upload", methods=["POST"])
def upload_file():
    password = request.form.get("password")
    file = request.files.get("file")
    if password != UPLOAD_PASSWORD:
        return "Mot de passe incorrect", 403
    if not file.filename.endswith(UPLOAD_ALLOWED_EXT):
        return "Extension non autorisée", 400
    file.save(os.path.join(DATA_DIR, file.filename))
    return "Upload réussi", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)