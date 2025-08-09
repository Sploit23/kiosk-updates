from flask import Flask, jsonify, send_from_directory, render_template, request
import os
import json
import sys
import requests
from datetime import datetime
import glob
from modules.printer import PrinterConfig
from modules.updater import UpdateManager

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
    with open(os.path.join(BASE_DIR, 'config', 'version.json')) as f:
        VERSION_INFO = json.load(f)
except FileNotFoundError:
    VERSION_INFO = {"version": "1.0.0", "update_url": "", "required_update": False}

# Tenta carregar as configurações do arquivo JSON
try:
    with open(os.path.join(BASE_DIR, 'config', 'settings.json')) as f:
        CONFIG = json.load(f)
    with open(os.path.join(BASE_DIR, 'config', 'themes.json')) as f:
        THEMES_CONFIG = json.load(f)
except FileNotFoundError:
    print("Erro: Arquivo de configuração não encontrado. Verifique se 'settings.json' e 'themes.json' existem na pasta config.")
    CONFIG = {"server": {"host": "0.0.0.0", "port": 5000, "debug": True}, "image_settings": {"base_path": "", "allowed_extensions": []}}
    THEMES_CONFIG = {"current_theme": "default", "available_themes": []}

# Inicializa módulos
printer_config = PrinterConfig()
update_manager = UpdateManager()

# Função para obter o caminho da pasta de imagens do dia atual
def get_images_folder_path():
    # Verifica se a pasta base existe
    base_path = CONFIG["image_settings"]["base_path"]
    if not os.path.exists(base_path):
        print(f"Aviso: Pasta base de imagens não encontrada: {base_path}")
        return base_path
    
    # Formata a data atual
    hoje = datetime.now()
    data_formatada = hoje.strftime("%d%m%Y")
    
    # Procura pela pasta com a data do dia
    images_dir = os.path.join(base_path, data_formatada)
    
    # Se a pasta do dia não existir, verifica se há outras pastas de data
    if not os.path.exists(images_dir):
        print(f"Aviso: Pasta do dia {data_formatada} não encontrada, procurando outras pastas de data...")
        try:
            # Lista todas as pastas na pasta base
            pastas = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
            # Filtra apenas pastas que parecem ser datas (8 dígitos)
            pastas_data = [p for p in pastas if p.isdigit() and len(p) == 8]
            
            if pastas_data:
                # Ordena por data mais recente
                pastas_data.sort(reverse=True)
                images_dir = os.path.join(base_path, pastas_data[0])
                print(f"Usando pasta mais recente encontrada: {pastas_data[0]}")
            else:
                print("Nenhuma pasta de data encontrada na pasta base.")
        except Exception as e:
            print(f"Erro ao procurar pastas de data: {str(e)}")
    
    return images_dir

@app.route("/")
def index():
    # Agora renderiza o template 'index.html' que está na pasta 'templates'
    return render_template("index.html")

@app.route("/config")
def config_page():
    # Página de configuração para selecionar pasta de imagens
    return render_template("config.html")

@app.route("/api/config")
def get_config():
    return jsonify({
        "server_config": CONFIG["server"],
        "image_settings": CONFIG["image_settings"],
        "themes": THEMES_CONFIG
    })

@app.route("/api/config/update", methods=["POST"])
def update_config():
    try:
        data = request.json
        if "image_path" in data:
            CONFIG["image_settings"]["base_path"] = data["image_path"]
            
            # Salva as configurações atualizadas no arquivo
            with open(os.path.join(BASE_DIR, 'config', 'settings.json'), 'w') as f:
                json.dump(CONFIG, f, indent=4)
                
            return jsonify({"status": "success", "message": "Configurações atualizadas com sucesso"})
        else:
            return jsonify({"status": "error", "message": "Caminho da pasta de imagens não fornecido"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao atualizar configurações: {str(e)}"}), 500

@app.route("/api/images")
def listar_imagens():
    images_dir = get_images_folder_path()
    
    if not os.path.exists(images_dir):
        return jsonify({
            "erro": f"Pasta de imagens '{os.path.basename(images_dir)}' não encontrada.",
            "pasta_base": CONFIG["image_settings"]["base_path"],
            "pasta_procurada": images_dir,
            "solucao": "Verifique se a pasta base está correta na página de configuração (/config)."
        }), 404

    imagens_agrupadas = {}
    try:
        arquivos = sorted(os.listdir(images_dir))
        arquivos_imagem = [f for f in arquivos if f.lower().endswith(tuple(CONFIG["image_settings"]["allowed_extensions"]))]
        
        if not arquivos_imagem:
            return jsonify({
                "erro": f"Nenhuma imagem encontrada na pasta '{os.path.basename(images_dir)}'.",
                "pasta_base": CONFIG["image_settings"]["base_path"],
                "pasta_atual": images_dir,
                "solucao": "Verifique se as imagens foram copiadas para a pasta correta."
            }), 404
            
        for f in arquivos_imagem:
            partes = f.split('_')
            if len(partes) >= 3:
                id_foto = partes[-1].split('.')[0]
                if id_foto not in imagens_agrupadas:
                    imagens_agrupadas[id_foto] = []
                imagens_agrupadas[id_foto].append(f)
            else:
                # Para imagens que não seguem o padrão de nomenclatura
                nome_base = os.path.splitext(f)[0]
                if nome_base not in imagens_agrupadas:
                    imagens_agrupadas[nome_base] = []
                imagens_agrupadas[nome_base].append(f)
    except Exception as e:
        return jsonify({
            "erro": f"Erro ao processar as imagens: {str(e)}",
            "pasta_base": CONFIG["image_settings"]["base_path"],
            "pasta_atual": images_dir,
            "solucao": "Verifique as permissões da pasta ou se o formato das imagens é suportado."
        }), 500
        
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