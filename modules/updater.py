import os
import sys
import json
import time
import shutil
import tempfile
import subprocess
import requests
from datetime import datetime

class Updater:
    def __init__(self, app_name="Kiosk de Fotos", update_url=None):
        self.app_name = app_name
        self.update_url = update_url or "https://example.com/updates/update_manifest.json"
        self.version_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "version.json")
        self.temp_dir = tempfile.mkdtemp(prefix=f"{app_name}_update_")
        self.current_version = self._get_current_version()
        self.is_frozen = getattr(sys, 'frozen', False)
        self.app_path = os.path.dirname(sys.executable) if self.is_frozen else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    def _get_current_version(self):
        """Obtém a versão atual do aplicativo"""
        try:
            with open(self.version_file, "r", encoding="utf-8") as f:
                version_data = json.load(f)
                return version_data.get("version", "1.0.0")
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existir ou for inválido, cria um novo
            self._create_default_version_file()
            return "1.0.0"
    
    def _create_default_version_file(self):
        """Cria um arquivo de versão padrão"""
        version_data = {
            "version": "1.0.0",
            "build_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "build_number": int(datetime.now().timestamp())
        }
        
        with open(self.version_file, "w", encoding="utf-8") as f:
            json.dump(version_data, f, indent=4)
    
    def check_for_updates(self):
        """Verifica se há atualizações disponíveis"""
        try:
            response = requests.get(self.update_url, timeout=10)
            if response.status_code == 200:
                update_data = response.json()
                latest_version = update_data.get("latest_version")
                min_compatible = update_data.get("min_compatible_version", "0.0.0")
                
                # Compara versões
                if self._compare_versions(latest_version, self.current_version) > 0:
                    # Verifica compatibilidade mínima
                    if self._compare_versions(self.current_version, min_compatible) >= 0:
                        return {
                            "status": "success",
                            "has_update": True,
                            "current_version": self.current_version,
                            "latest_version": latest_version,
                            "download_url": update_data.get("download_url"),
                            "changelog": update_data.get("changelog", []),
                            "is_mandatory": update_data.get("is_mandatory", False),
                            "message": update_data.get("message", "Nova versão disponível!")
                        }
                    else:
                        return {
                            "status": "error",
                            "message": "Versão atual incompatível com a atualização. É necessário baixar manualmente a nova versão.",
                            "has_update": False
                        }
                else:
                    return {
                        "status": "success",
                        "has_update": False,
                        "current_version": self.current_version,
                        "latest_version": latest_version
                    }
            else:
                return {
                    "status": "error",
                    "message": f"Erro ao verificar atualizações: {response.status_code}",
                    "has_update": False
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao verificar atualizações: {str(e)}",
                "has_update": False
            }
    
    def _compare_versions(self, version1, version2):
        """Compara duas versões no formato X.Y.Z"""
        v1_parts = [int(x) for x in version1.split('.')]
        v2_parts = [int(x) for x in version2.split('.')]
        
        # Garante que ambas as listas tenham o mesmo tamanho
        while len(v1_parts) < 3:
            v1_parts.append(0)
        while len(v2_parts) < 3:
            v2_parts.append(0)
        
        # Compara cada parte da versão
        for i in range(3):
            if v1_parts[i] > v2_parts[i]:
                return 1  # version1 é maior
            elif v1_parts[i] < v2_parts[i]:
                return -1  # version2 é maior
        
        return 0  # versões são iguais
    
    def download_update(self, download_url):
        """Baixa a atualização para um diretório temporário"""
        try:
            # Cria um nome de arquivo baseado na URL
            file_name = os.path.basename(download_url)
            download_path = os.path.join(self.temp_dir, file_name)
            
            # Baixa o arquivo
            response = requests.get(download_url, stream=True, timeout=60)
            if response.status_code == 200:
                with open(download_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                return {
                    "status": "success",
                    "file_path": download_path
                }
            else:
                return {
                    "status": "error",
                    "message": f"Erro ao baixar atualização: {response.status_code}"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao baixar atualização: {str(e)}"
            }
    
    def apply_update(self, file_path):
        """Aplica a atualização baixada"""
        # Esta função só funciona se o aplicativo estiver em modo frozen (executável)
        if not self.is_frozen:
            return {
                "status": "error",
                "message": "A atualização automática só funciona no modo executável."
            }
        
        try:
            # Verifica se o arquivo existe
            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "message": "Arquivo de atualização não encontrado."
                }
            
            # Cria um script de atualização que será executado após o fechamento do aplicativo
            update_script = self._create_update_script(file_path)
            
            # Executa o script de atualização
            if sys.platform == "win32":
                subprocess.Popen(["cmd", "/c", update_script], 
                               shell=True, 
                               creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(["bash", update_script])
            
            return {
                "status": "success",
                "message": "Atualização iniciada. O aplicativo será reiniciado."
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao aplicar atualização: {str(e)}"
            }
    
    def _create_update_script(self, update_file):
        """Cria um script para aplicar a atualização após o fechamento do aplicativo"""
        # Cria um arquivo de script temporário
        if sys.platform == "win32":
            script_path = os.path.join(self.temp_dir, "update.bat")
            
            # Conteúdo do script batch para Windows
            script_content = f"""
@echo off
echo Aguardando o fechamento do aplicativo...
timeout /t 2 /nobreak > nul

echo Aplicando atualização...
start /wait "" "{update_file}"

echo Limpando arquivos temporários...
rd /s /q "{self.temp_dir}"

echo Atualização concluída!
start "" "{os.path.join(self.app_path, self.app_name + '.exe')}"

del "%~f0"
"""
        else:
            script_path = os.path.join(self.temp_dir, "update.sh")
            
            # Conteúdo do script shell para Unix/Linux
            script_content = f"""
#!/bin/bash
echo "Aguardando o fechamento do aplicativo..."
sleep 2

echo "Aplicando atualização..."
chmod +x "{update_file}"
"{update_file}"

echo "Limpando arquivos temporários..."
rm -rf "{self.temp_dir}"

echo "Atualização concluída!"
"{os.path.join(self.app_path, self.app_name)}"

rm "$0"
"""
            
            # Torna o script executável
            os.chmod(script_path, 0o755)
        
        # Escreve o conteúdo no arquivo
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        
        return script_path
    
    def cleanup(self):
        """Limpa arquivos temporários"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"Erro ao limpar arquivos temporários: {str(e)}")

# Instância global do atualizador
updater = Updater()

# Função para verificar atualizações
def check_for_updates():
    return updater.check_for_updates()

# Função para baixar e aplicar atualizações
def download_and_apply_update(download_url):
    download_result = updater.download_update(download_url)
    
    if download_result["status"] == "success":
        return updater.apply_update(download_result["file_path"])
    else:
        return download_result

# Função para obter a versão atual
def get_current_version():
    return updater.current_version