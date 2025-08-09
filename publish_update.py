#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para facilitar a publicação de atualizações no repositório GitHub.
Este script atualiza o arquivo update_manifest.json com as informações da nova versão.
"""

import os
import sys
import json
import hashlib
import argparse
from datetime import datetime

def calculate_file_hash(file_path):
    """Calcula o hash SHA-256 de um arquivo"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Lê o arquivo em blocos de 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def update_manifest(version, installer_path, min_compatible_version=None, is_mandatory=False, message=None, changelog=None):
    """Atualiza o arquivo update_manifest.json com as informações da nova versão"""
    # Caminho para o arquivo de manifesto
    manifest_path = "update_manifest.json"
    
    # Verifica se o arquivo de manifesto existe
    if os.path.exists(manifest_path):
        # Carrega o manifesto existente
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    else:
        # Cria um novo manifesto
        manifest = {}
    
    # Nome do arquivo do instalador
    installer_filename = os.path.basename(installer_path)
    
    # URL de download no GitHub
    download_url = f"https://github.com/Sploit23/kiosk-updates/releases/download/v{version}/kiosk_photo_{version}.exe"
    
    # Atualiza as informações do manifesto
    manifest["latest_version"] = version
    manifest["download_url"] = download_url
    manifest["release_date"] = datetime.now().strftime("%Y-%m-%d")
    
    # Calcula o hash do instalador
    file_hash = calculate_file_hash(installer_path)
    manifest["signature"] = f"sha256:{file_hash}"
    
    # Atualiza a versão mínima compatível se fornecida
    if min_compatible_version:
        manifest["min_compatible_version"] = min_compatible_version
    elif "min_compatible_version" not in manifest:
        manifest["min_compatible_version"] = version
    
    # Atualiza se a atualização é obrigatória
    manifest["is_mandatory"] = is_mandatory
    
    # Atualiza a mensagem se fornecida
    if message:
        manifest["message"] = message
    elif "message" not in manifest:
        manifest["message"] = "Nova versão disponível com melhorias importantes!"
    
    # Atualiza o changelog se fornecido
    if changelog:
        manifest["changelog"] = changelog
    elif "changelog" not in manifest:
        manifest["changelog"] = [f"Versão {version} lançada"]
    
    # Salva o manifesto atualizado
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)
    
    print(f"Manifesto atualizado com sucesso para a versão {version}!")
    print(f"URL de download: {download_url}")
    print(f"Hash do arquivo: {file_hash}")
    print("\nPróximos passos:")
    print("1. Crie uma tag/release no GitHub com o nome v{version}")
    print("2. Faça upload do instalador para a release")
    print("3. Faça commit e push do arquivo update_manifest.json atualizado")

def main():
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description="Atualiza o manifesto de atualização com uma nova versão")
    parser.add_argument("version", help="Número da nova versão (ex: 1.1.0)")
    parser.add_argument("installer_path", help="Caminho para o arquivo do instalador")
    parser.add_argument("--min-version", help="Versão mínima compatível (ex: 1.0.0)")
    parser.add_argument("--mandatory", action="store_true", help="Define se a atualização é obrigatória")
    parser.add_argument("--message", help="Mensagem a ser exibida para o usuário")
    parser.add_argument("--changelog", nargs="+", help="Lista de mudanças na nova versão")
    
    # Analisa os argumentos
    args = parser.parse_args()
    
    # Verifica se o arquivo do instalador existe
    if not os.path.exists(args.installer_path):
        print(f"Erro: O arquivo {args.installer_path} não existe!")
        return 1
    
    # Atualiza o manifesto
    update_manifest(
        args.version,
        args.installer_path,
        args.min_version,
        args.mandatory,
        args.message,
        args.changelog
    )
    
    return 0

if __name__ == "__main__":
    sys.exit(main())