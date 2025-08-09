@echo off
echo ===================================
echo    INICIANDO KIOSK DE FOTOS
echo ===================================
echo.

:: Verifica se o ambiente virtual existe
IF NOT EXIST venv (
    echo Criando ambiente virtual...
    python -m venv venv
    echo Ambiente virtual criado!
    echo.
    
    echo Instalando dependencias...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo Dependencias instaladas!
    echo.
) ELSE (
    echo Ambiente virtual encontrado.
    call venv\Scripts\activate.bat
    echo.
)

:: Inicia o servidor
echo Iniciando o servidor...
echo.
echo Pressione Ctrl+C para encerrar o servidor.
echo.
python server.py

:: Desativa o ambiente virtual ao sair
call venv\Scripts\deactivate.bat