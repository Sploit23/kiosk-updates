# -*- coding: utf-8 -*-
"""
Módulo de configuração da impressora
Gerencia as configurações e operações relacionadas à impressão
"""

import json
import os
from typing import Dict, Any, Optional

class PrinterConfig:
    """Classe para gerenciar configurações da impressora"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join('config', 'printer_settings.json')
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Carrega as configurações da impressora do arquivo JSON"""
        default_settings = {
            'printer_name': 'default',
            'paper_size': 'A4',
            'orientation': 'portrait',
            'quality': 'high',
            'margins': {
                'top': 10,
                'bottom': 10,
                'left': 10,
                'right': 10
            },
            'scale': 'fit_to_page',
            'color_mode': 'color'
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                # Mescla com configurações padrão para garantir que todas as chaves existam
                return {**default_settings, **settings}
            else:
                # Cria arquivo com configurações padrão se não existir
                self.save_settings(default_settings)
                return default_settings
        except Exception as e:
            print(f"Erro ao carregar configurações da impressora: {e}")
            return default_settings
    
    def save_settings(self, settings: Dict[str, Any] = None) -> bool:
        """Salva as configurações da impressora no arquivo JSON"""
        try:
            settings_to_save = settings or self.settings
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(settings_to_save, f, indent=4, ensure_ascii=False)
            
            if settings:
                self.settings = settings
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações da impressora: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Obtém uma configuração específica"""
        return self.settings.get(key, default)
    
    def update_setting(self, key: str, value: Any) -> bool:
        """Atualiza uma configuração específica"""
        try:
            self.settings[key] = value
            return self.save_settings()
        except Exception as e:
            print(f"Erro ao atualizar configuração {key}: {e}")
            return False
    
    def get_print_options(self) -> Dict[str, Any]:
        """Retorna opções formatadas para impressão"""
        return {
            'printer': self.settings.get('printer_name', 'default'),
            'paperSize': self.settings.get('paper_size', 'A4'),
            'orientation': self.settings.get('orientation', 'portrait'),
            'quality': self.settings.get('quality', 'high'),
            'margins': self.settings.get('margins', {}),
            'scale': self.settings.get('scale', 'fit_to_page'),
            'colorMode': self.settings.get('color_mode', 'color')
        }