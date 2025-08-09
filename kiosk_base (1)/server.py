from flask import Flask, jsonify, send_from_directory, render_template
import os

app = Flask(__name__, template_folder=".")

# Pasta onde ficam as imagens
IMG_FOLDER = "imagens"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/imagens")
def listar_imagens():
    arquivos = sorted(os.listdir(IMG_FOLDER))
    imagens = [f for f in arquivos if f.lower().endswith(".jpg")]
    return jsonify(imagens)

@app.route("/imagens/<path:nome>")
def servir_imagem(nome):
    return send_from_directory(IMG_FOLDER, nome)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
