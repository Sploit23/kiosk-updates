import os
import sys
import json
import shutil
import subprocess
from datetime import datetime

# Configurações
APP_NAME = "Kiosk de Fotos"
APP_VERSION = "1.0.0"
OUTPUT_DIR = "dist"
BUILD_DIR = "build"
ICON_PATH = "static/icon.ico"  # Certifique-se de ter um ícone

# Verifica se o PyInstaller está instalado
try:
    import PyInstaller
except ImportError:
    print("PyInstaller não está instalado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

# Carrega a versão atual do arquivo version.json
def load_version():
    try:
        with open("version.json", "r", encoding="utf-8") as f:
            version_data = json.load(f)
            return version_data.get("version", "1.0.0")
    except (FileNotFoundError, json.JSONDecodeError):
        return "1.0.0"

# Atualiza o arquivo version.json com a nova versão
def update_version(version):
    version_data = {
        "version": version,
        "build_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "build_number": int(datetime.now().timestamp())
    }
    
    with open("version.json", "w", encoding="utf-8") as f:
        json.dump(version_data, f, indent=4)

# Cria o executável com PyInstaller
def build_executable(version):
    print(f"Construindo executável para {APP_NAME} v{version}...")
    
    # Limpa diretórios de build anteriores
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    
    # Arquivos e diretórios a serem incluídos
    data_files = [
        ("templates", "templates"),
        ("static", "static"),
        ("modules", "modules"),
        ("config", "config"),
        ("requirements.txt", ".")
    ]
    
    # Constrói a string de dados para PyInstaller
    datas_str = ""
    for src, dst in data_files:
        datas_str += f"--add-data {src}{os.pathsep}{dst} "
    
    # Comando PyInstaller
    icon_param = f"--icon={ICON_PATH}" if os.path.exists(ICON_PATH) else ""
    cmd = f"pyinstaller --name=\"{APP_NAME}\" --onefile {icon_param} {datas_str} --windowed server.py"
    
    print(f"Executando comando: {cmd}")
    subprocess.check_call(cmd, shell=True)
    
    print(f"Executável criado com sucesso em {OUTPUT_DIR}/{APP_NAME}.exe")

# Cria um instalador simples (opcional)
def create_installer(version):
    # Aqui você pode adicionar código para criar um instalador
    # Usando ferramentas como NSIS, Inno Setup, etc.
    print("Criação de instalador não implementada neste script.")
    print("Você pode usar ferramentas como NSIS ou Inno Setup para criar um instalador.")

# Função principal
def main():
    # Obtém a versão atual ou usa a padrão
    current_version = load_version()
    
    # Pergunta se deseja atualizar a versão
    print(f"Versão atual: {current_version}")
    update_version_input = input("Deseja atualizar a versão? (s/n): ").lower()
    
    if update_version_input == "s":
        new_version = input("Digite a nova versão (ex: 1.0.1): ")
        update_version(new_version)
        version = new_version
    else:
        version = current_version
    
    # Constrói o executável
    build_executable(version)
    
    # Pergunta se deseja criar um instalador
    create_installer_input = input("Deseja criar um instalador? (s/n): ").lower()
    if create_installer_input == "s":
        create_installer(version)
    
    print(f"\nProcesso concluído para {APP_NAME} v{version}")
    print(f"O executável está disponível em: {os.path.abspath(os.path.join(OUTPUT_DIR, APP_NAME + '.exe'))}")

if __name__ == "__main__":
    main()