#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para testar o sistema de atualização do Kiosk Photo.
Este script verifica se o sistema de atualização está funcionando corretamente.
"""

import os
import sys
import json
import requests
from datetime import datetime

# Adiciona o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa o módulo de atualização
try:
    from modules.updater import Updater
except ImportError:
    print("Erro: Não foi possível importar o módulo de atualização.")
    print("Certifique-se de que o arquivo 'modules/updater.py' existe.")
    sys.exit(1)

def test_version_file():
    """Testa se o arquivo version.json existe e está correto"""
    print("\n[Teste 1] Verificando arquivo version.json...")
    
    version_file = "version.json"
    if not os.path.exists(version_file):
        print("  [FALHA] Arquivo version.json não encontrado!")
        return False
    
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            version_data = json.load(f)
        
        # Verifica se os campos obrigatórios existem
        required_fields = ["version", "build_date", "update_url"]
        for field in required_fields:
            if field not in version_data:
                print(f"  [FALHA] Campo '{field}' não encontrado no arquivo version.json!")
                return False
        
        print(f"  [OK] Arquivo version.json encontrado e válido.")
        print(f"  Versão atual: {version_data['version']}")
        print(f"  URL de atualização: {version_data['update_url']}")
        return True
    except json.JSONDecodeError:
        print("  [FALHA] Arquivo version.json não é um JSON válido!")
        return False
    except Exception as e:
        print(f"  [FALHA] Erro ao ler o arquivo version.json: {str(e)}")
        return False

def test_updater_module():
    """Testa se o módulo de atualização está funcionando corretamente"""
    print("\n[Teste 2] Verificando módulo de atualização...")
    
    try:
        # Cria uma instância do atualizador
        updater = Updater()
        
        # Verifica se a versão atual foi carregada corretamente
        if not updater.current_version:
            print("  [FALHA] Não foi possível obter a versão atual!")
            return False
        
        print(f"  [OK] Módulo de atualização carregado com sucesso.")
        print(f"  Versão atual: {updater.current_version}")
        print(f"  URL do manifesto: {updater.update_url}")
        return True
    except Exception as e:
        print(f"  [FALHA] Erro ao inicializar o módulo de atualização: {str(e)}")
        return False

def test_manifest_url():
    """Testa se a URL do manifesto está acessível"""
    print("\n[Teste 3] Verificando acesso à URL do manifesto...")
    
    try:
        # Cria uma instância do atualizador
        updater = Updater()
        
        # Tenta acessar a URL do manifesto
        try:
            response = requests.get(updater.update_url, timeout=10)
            if response.status_code == 200:
                try:
                    manifest_data = response.json()
                    print(f"  [OK] URL do manifesto acessível e válida.")
                    print(f"  Versão mais recente: {manifest_data.get('latest_version', 'N/A')}")
                    print(f"  URL de download: {manifest_data.get('download_url', 'N/A')}")
                    return True
                except json.JSONDecodeError:
                    print("  [FALHA] O conteúdo da URL não é um JSON válido!")
                    return False
            else:
                print(f"  [FALHA] Não foi possível acessar a URL do manifesto! Código de status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"  [FALHA] Erro ao acessar a URL do manifesto: {str(e)}")
            return False
    except Exception as e:
        print(f"  [FALHA] Erro ao inicializar o módulo de atualização: {str(e)}")
        return False

def test_check_for_updates():
    """Testa a função de verificação de atualizações"""
    print("\n[Teste 4] Testando verificação de atualizações...")
    
    try:
        # Cria uma instância do atualizador
        updater = Updater()
        
        # Verifica se há atualizações disponíveis
        update_info = updater.check_for_updates()
        
        if update_info["status"] == "success":
            if update_info["has_update"]:
                print(f"  [OK] Atualização disponível!")
                print(f"  Versão atual: {update_info['current_version']}")
                print(f"  Versão mais recente: {update_info['latest_version']}")
                print(f"  URL de download: {update_info['download_url']}")
                print(f"  Changelog: {', '.join(update_info['changelog'])}")
            else:
                print(f"  [OK] Nenhuma atualização disponível.")
                print(f"  Versão atual: {update_info['current_version']}")
                print(f"  Versão mais recente: {update_info['latest_version']}")
            return True
        else:
            print(f"  [FALHA] Erro ao verificar atualizações: {update_info['message']}")
            return False
    except Exception as e:
        print(f"  [FALHA] Erro ao verificar atualizações: {str(e)}")
        return False

def main():
    """Função principal"""
    print("====================================================")
    print("Teste do Sistema de Atualização do Kiosk Photo")
    print("====================================================")
    print(f"Data e hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("====================================================")
    
    # Executa os testes
    tests = [
        test_version_file,
        test_updater_module,
        test_manifest_url,
        test_check_for_updates
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Exibe o resumo dos testes
    print("\n====================================================")
    print("Resumo dos Testes")
    print("====================================================")
    
    for i, result in enumerate(results):
        test_name = tests[i].__name__.replace("test_", "").replace("_", " ").title()
        status = "PASSOU" if result else "FALHOU"
        print(f"[{i+1}] {test_name}: {status}")
    
    # Verifica se todos os testes passaram
    if all(results):
        print("\n[SUCESSO] Todos os testes passaram! O sistema de atualização está funcionando corretamente.")
        return 0
    else:
        print("\n[FALHA] Alguns testes falharam! Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())