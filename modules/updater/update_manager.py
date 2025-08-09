# -*- coding: utf-8 -*-
"""
Módulo de gerenciamento de atualizações
Gerencia verificação e aplicação de atualizações do sistema
"""

import json
import os
import requests
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

class UpdateManager:
    """Classe para gerenciar atualizações do sistema"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join('config', 'version.json')
        self.version_info = self.load_version_info()
    
    def load_version_info(self) -> Dict[str, Any]:
        """Carrega informações de versão do arquivo JSON"""
        default_version = {
            'version': '1.0.0',
            'build_date': datetime.now().isoformat(),
            'last_update_check': None,
            'update_url': None,
            'auto_update': False
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    version_info = json.load(f)
                return {**default_version, **version_info}
            else:
                self.save_version_info(default_version)
                return default_version
        except Exception as e:
            print(f"Erro ao carregar informações de versão: {e}")
            return default_version
    
    def save_version_info(self, version_info: Dict[str, Any] = None) -> bool:
        """Salva informações de versão no arquivo JSON"""
        try:
            info_to_save = version_info or self.version_info
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(info_to_save, f, indent=4, ensure_ascii=False)
            
            if version_info:
                self.version_info = version_info
            return True
        except Exception as e:
            print(f"Erro ao salvar informações de versão: {e}")
            return False
    
    def get_current_version(self) -> str:
        """Retorna a versão atual do sistema"""
        return self.version_info.get('version', '1.0.0')
    
    def check_for_updates(self, update_url: str = None) -> Tuple[bool, Optional[Dict]]:
        """Verifica se há atualizações disponíveis"""
        try:
            url = update_url or self.version_info.get('update_url')
            if not url:
                return False, None
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            remote_info = response.json()
            current_version = self.get_current_version()
            remote_version = remote_info.get('version', '1.0.0')
            
            # Atualiza timestamp da última verificação
            self.version_info['last_update_check'] = datetime.now().isoformat()
            self.save_version_info()
            
            # Compara versões (implementação simples)
            if self._compare_versions(remote_version, current_version) > 0:
                return True, remote_info
            
            return False, None
            
        except Exception as e:
            print(f"Erro ao verificar atualizações: {e}")
            return False, None
    
    def _compare_versions(self, version1: str, version2: str) -> int:
        """Compara duas versões. Retorna 1 se version1 > version2, -1 se version1 < version2, 0 se iguais"""
        try:
            v1_parts = [int(x) for x in version1.split('.')]
            v2_parts = [int(x) for x in version2.split('.')]
            
            # Normaliza o tamanho das listas
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))
            
            for i in range(max_len):
                if v1_parts[i] > v2_parts[i]:
                    return 1
                elif v1_parts[i] < v2_parts[i]:
                    return -1
            
            return 0
        except Exception:
            return 0
    
    def update_version(self, new_version: str) -> bool:
        """Atualiza a versão atual do sistema"""
        try:
            self.version_info['version'] = new_version
            self.version_info['build_date'] = datetime.now().isoformat()
            return self.save_version_info()
        except Exception as e:
            print(f"Erro ao atualizar versão: {e}")
            return False
    
    def get_update_info(self) -> Dict[str, Any]:
        """Retorna informações sobre atualizações"""
        return {
            'current_version': self.get_current_version(),
            'last_check': self.version_info.get('last_update_check'),
            'auto_update': self.version_info.get('auto_update', False),
            'update_url': self.version_info.get('update_url')
        }