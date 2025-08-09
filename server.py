from flask import Flask, jsonify, send_from_directory, render_template, request
import os
import json
import sys
import requests
from datetime import datetime

# Importa o módulo de impressão
try:
    from modules.printer import Printer
    PRINTER_AVAILABLE = True
except ImportError:
    print("Aviso: Módulo de impressão não disponível. Funcionalidade de impressão será limitada.")
    PRINTER_AVAILABLE = False

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carrega informações de versão
try:
    with open(os.path.join(BASE_DIR, 'version.json')) as f:
        VERSION_INFO = json.load(f)
except FileNotFoundError:
    VERSION_INFO = {"version": "1.0.0", "update_url": "", "required_update": False}

# Tenta carregar as configurações do arquivo JSON
try:
    with open(os.path.join(BASE_DIR, 'settings.json')) as f:
        CONFIG = json.load(f)
    with open(os.path.join(BASE_DIR, 'themes.json')) as f:
        THEMES_CONFIG = json.load(f)
except FileNotFoundError:
    print("Erro: Arquivo de configuração não encontrado. Verifique se 'settings.json' e 'themes.json' existem.")
    CONFIG = {"server": {"host": "0.0.0.0", "port": 5000, "debug": True}, "image_settings": {"base_path": "", "allowed_extensions": []}}
    THEMES_CONFIG = {"current_theme": "default", "available_themes": []}

# Função para obter o caminho da pasta de imagens do dia atual
def get_images_folder_path():
    hoje = datetime.now()
    data_formatada = hoje.strftime("%d%m%Y")
    images_dir = os.path.join(CONFIG["image_settings"]["base_path"], data_formatada)
    return images_dir

@app.route("/")
def index():
    # Agora renderiza o template 'index.html' que está na pasta 'templates'
    return render_template("index.html")

@app.route("/api/config")
def get_config():
    return jsonify({
        "server_config": CONFIG["server"],
        "image_settings": CONFIG["image_settings"],
        "themes": THEMES_CONFIG
    })

@app.route("/api/images")
def listar_imagens():
    images_dir = get_images_folder_path()
    
    if not os.path.exists(images_dir):
        return jsonify({"erro": f"Pasta de imagens do dia '{os.path.basename(images_dir)}' não encontrada."}), 404

    imagens_agrupadas = {}
    try:
        arquivos = sorted(os.listdir(images_dir))
        for f in arquivos:
            if f.lower().endswith(tuple(CONFIG["image_settings"]["allowed_extensions"])):
                partes = f.split('_')
                if len(partes) >= 3:
                    id_foto = partes[-1].split('.')[0]
                    if id_foto not in imagens_agrupadas:
                        imagens_agrupadas[id_foto] = []
                    imagens_agrupadas[id_foto].append(f)
    except Exception as e:
        return jsonify({"erro": f"Erro ao processar as imagens: {str(e)}"}), 500
        
    return jsonify(imagens_agrupadas)

@app.route("/imagens/<path:nome>")
def servir_imagem(nome):
    images_dir = get_images_folder_path()
    return send_from_directory(images_dir, nome)

# Adiciona rota para servir arquivos estáticos, incluindo temas
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'static'), filename)

# API para obter informações de versão
@app.route('/api/version')
def get_version():
    return jsonify(VERSION_INFO)

# API para verificar atualizações
@app.route('/api/check-update')
def check_update():
    try:
        # Verifica se há uma URL de atualização configurada
        if not VERSION_INFO.get('update_url'):
            return jsonify({"status": "error", "message": "URL de atualização não configurada"}), 400
            
        # Faz requisição para o servidor de atualizações
        response = requests.get(f"{VERSION_INFO['update_url']}/manifest.json", timeout=5)
        if response.status_code != 200:
            return jsonify({"status": "error", "message": "Erro ao verificar atualizações"}), 500
            
        manifest = response.json()
        current_version = VERSION_INFO.get('version', '1.0.0')
        latest_version = manifest.get('latest_version')
        
        # Compara versões
        has_update = latest_version != current_version
        
        return jsonify({
            "status": "success",
            "current_version": current_version,
            "latest_version": latest_version,
            "has_update": has_update,
            "required_update": manifest.get('required_update', False),
            "download_url": manifest.get('download_url', ''),
            "changelog": manifest.get('changelog', [])
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao verificar atualizações: {str(e)}"}), 500

# API para listar impressoras disponíveis
@app.route('/api/printers')
def list_printers():
    if not PRINTER_AVAILABLE:
        return jsonify({"status": "error", "message": "Módulo de impressão não disponível"}), 503
    
    try:
        printer_config = {}
        if "printer" in CONFIG:
            printer_config = CONFIG["printer"]
        
        printer = Printer(printer_config)
        printers = printer.available_printers
        default_printer = printer._get_default_printer()
        
        return jsonify({
            "status": "success",
            "printers": printers,
            "default_printer": default_printer
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao listar impressoras: {str(e)}"}), 500

# API para imprimir imagem
@app.route('/api/print', methods=['POST'])
def print_image():
    if not PRINTER_AVAILABLE:
        return jsonify({"status": "error", "message": "Módulo de impressão não disponível"}), 503
    
    try:
        data = request.json
        if not data or 'image_path' not in data:
            return jsonify({"status": "error", "message": "Caminho da imagem não fornecido"}), 400
        
        image_name = data['image_path']
        printer_name = data.get('printer_name', 'auto')
        
        # Obtém o caminho completo da imagem
        images_dir = get_images_folder_path()
        image_path = os.path.join(images_dir, image_name)
        
        if not os.path.exists(image_path):
            return jsonify({"status": "error", "message": f"Imagem não encontrada: {image_name}"}), 404
        
        # Configura e usa o módulo de impressão
        printer_config = {}
        if "printer" in CONFIG:
            printer_config = CONFIG["printer"]
            
        printer = Printer(printer_config)
        result = printer.print_image(image_path, printer_name)
        
        return jsonify({
            "status": "sent",
            "printer": result.get("printer", printer_name),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao imprimir: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(
        host=CONFIG["server"]["host"],
        port=CONFIG["server"]["port"],
        debug=CONFIG["server"]["debug"]
    )