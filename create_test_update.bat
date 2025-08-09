@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo Criacao de Atualizacao de Teste para o Kiosk Photo
echo ===================================================
echo.

REM Define a nova versão
set NEW_VERSION=1.0.1

REM Verifica se o arquivo version.json existe
if not exist "version.json" (
    echo Erro: Arquivo version.json nao encontrado!
    pause
    exit /b 1
)

echo Atualizando version.json para a versao %NEW_VERSION%...

REM Cria um arquivo temporário
set TEMP_FILE=version_temp.json

REM Lê o arquivo version.json e atualiza a versão
type version.json > %TEMP_FILE%

REM Substitui a versão no arquivo temporário
powershell -Command "(Get-Content %TEMP_FILE%) -replace '\"version\": \"[0-9\.]+\"', '\"version\": \"%NEW_VERSION%\"' | Set-Content %TEMP_FILE%"

REM Substitui o arquivo original pelo temporário
move /y %TEMP_FILE% version.json > nul

echo Versao atualizada com sucesso!
echo.

REM Verifica se o PyInstaller está instalado
python -c "import PyInstaller" > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Erro: PyInstaller nao encontrado. Instalando...
    pip install pyinstaller
    if %ERRORLEVEL% neq 0 (
        echo Erro: Falha ao instalar PyInstaller!
        pause
        exit /b 1
    )
)

echo Gerando executavel com PyInstaller...

REM Executa o script build_executable.py
python build_executable.py
if %ERRORLEVEL% neq 0 (
    echo Erro: Falha ao gerar o executavel!
    pause
    exit /b 1
)

echo Executavel gerado com sucesso!
echo.

REM Verifica se o Inno Setup está instalado
where iscc > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Aviso: Inno Setup nao encontrado. O instalador nao sera gerado.
    echo Por favor, instale o Inno Setup e execute o script installer_script.iss manualmente.
    echo.
    echo Voce pode baixar o Inno Setup em: https://jrsoftware.org/isdl.php
) else (
    echo Gerando instalador com Inno Setup...
    
    REM Atualiza a versão no script do Inno Setup
    set TEMP_ISS=installer_temp.iss
    type installer_script.iss > %TEMP_ISS%
    powershell -Command "(Get-Content %TEMP_ISS%) -replace '#define MyAppVersion \"[0-9\.]+\"', '#define MyAppVersion \"%NEW_VERSION%\"' | Set-Content %TEMP_ISS%"
    
    REM Compila o instalador
    iscc %TEMP_ISS%
    if %ERRORLEVEL% neq 0 (
        echo Erro: Falha ao gerar o instalador!
        del %TEMP_ISS%
        pause
        exit /b 1
    )
    
    del %TEMP_ISS%
    
    echo Instalador gerado com sucesso!
    echo.
    
    REM Copia o instalador para a pasta de releases
    if not exist "releases" mkdir releases
    copy /y "Output\kiosk_photo_setup.exe" "releases\kiosk_photo_%NEW_VERSION%.exe" > nul
    
    echo Instalador copiado para releases\kiosk_photo_%NEW_VERSION%.exe
)

echo.
echo ===================================================
echo Atualizacao de teste criada com sucesso!
echo ===================================================
echo.
echo Proximos passos:
echo 1. Execute o script publish_update.py para atualizar o manifesto:
 echo    python publish_update.py %NEW_VERSION% releases\kiosk_photo_%NEW_VERSION%.exe --changelog "Versao de teste" "Correcao de bugs"
echo 2. Teste o sistema de atualizacao executando test_update_system.py
echo.

pause