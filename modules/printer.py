import os
import platform
import subprocess
import win32print
import win32api
from PIL import Image

class Printer:
    def __init__(self, config):
        self.config = config
        self.available_printers = self._get_available_printers()
        
    def _get_available_printers(self):
        """Lista todas as impressoras disponíveis"""
        if platform.system() == 'Windows':
            return [printer[2] for printer in win32print.EnumPrinters(2)]
        else:
            # Para Linux/Mac
            try:
                result = subprocess.run(['lpstat', '-a'], capture_output=True, text=True)
                return [line.split()[0] for line in result.stdout.splitlines()]
            except:
                return []
    
    def print_image(self, image_path, printer_name=None):
        """Imprime uma imagem na impressora especificada"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        printer_name = printer_name or self.config.get('default_printer')
        if printer_name == 'auto':
            printer_name = self._get_default_printer()
        
        # Verifica se a impressora existe
        if printer_name not in self.available_printers:
            raise ValueError(f"Printer not available: {printer_name}")
        
        # Valida a imagem
        try:
            with Image.open(image_path) as img:
                img.verify()
        except Exception as e:
            raise ValueError(f"Invalid image file: {str(e)}")
        
        # Comando de impressão específico por SO
        if platform.system() == 'Windows':
            return self._print_windows(image_path, printer_name)
        else:
            return self._print_unix(image_path, printer_name)
    
    def _print_windows(self, image_path, printer_name):
        """Imprime no Windows"""
        try:
            win32api.ShellExecute(
                0,
                "print",
                image_path,
                f'/d:"{printer_name}"',
                ".",
                0
            )
            return {
                "status": "sent",
                "printer": printer_name,
                "system": "windows"
            }
        except Exception as e:
            raise RuntimeError(f"Windows print error: {str(e)}")
    
    def _print_unix(self, image_path, printer_name):
        """Imprime em sistemas Unix-like (Linux/Mac)"""
        try:
            cmd = [
                'lp',
                '-d', printer_name,
                image_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise RuntimeError(result.stderr)
            
            return {
                "status": "sent",
                "printer": printer_name,
                "system": "unix",
                "job_id": result.stdout.strip()
            }
        except Exception as e:
            raise RuntimeError(f"Unix print error: {str(e)}")
    
    def _get_default_printer(self):
        """Obtém a impressora padrão do sistema"""
        if platform.system() == 'Windows':
            return win32print.GetDefaultPrinter()
        else:
            try:
                result = subprocess.run(['lpstat', '-d'], capture_output=True, text=True)
                return result.stdout.split(':')[-1].strip()
            except:
                return None