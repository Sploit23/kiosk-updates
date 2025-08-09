@echo off
echo ===================================================
echo Configuracao do Repositorio de Atualizacoes do Kiosk Photo
echo ===================================================
echo.

REM Verifica se o Git está instalado
git --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Erro: Git nao encontrado. Por favor, instale o Git antes de continuar.
    echo Voce pode baixar o Git em: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo Git encontrado. Continuando...
echo.

REM Verifica se já existe um repositório Git
if exist ".git" (
    echo Repositorio Git ja inicializado.
) else (
    echo Inicializando repositorio Git...
    git init
    echo Repositorio Git inicializado com sucesso.
)

echo.

REM Verifica se o remote já está configurado
git remote -v | findstr "origin" > nul
if %ERRORLEVEL% equ 0 (
    echo Remote 'origin' ja configurado.
) else (
    echo Configurando remote 'origin'...
    git remote add origin https://github.com/Sploit23/kiosk-updates.git
    echo Remote 'origin' configurado com sucesso.
)

echo.

REM Cria a estrutura de diretórios
if not exist "releases" (
    echo Criando diretorio 'releases'...
    mkdir releases
    echo Diretorio 'releases' criado com sucesso.
) else (
    echo Diretorio 'releases' ja existe.
)

echo.

REM Verifica se o arquivo update_manifest.json existe
if exist "update_manifest.json" (
    echo Arquivo 'update_manifest.json' ja existe.
) else (
    echo Criando arquivo 'update_manifest.json'...
    echo {
    echo     "latest_version": "1.0.0",
    echo     "min_compatible_version": "0.9.0",
    echo     "download_url": "https://github.com/Sploit23/kiosk-updates/releases/download/v1.0.0/kiosk_photo_1.0.0.exe",
    echo     "changelog": [
    echo         "Integracao completa com sistema de impressao",
    echo         "Interface melhorada com tema de Natal",
    echo         "Correcao de bugs na exibicao de miniaturas",
    echo         "Adicionado sistema de atualizacao automatica"
    echo     ],
    echo     "release_date": "2023-12-15",
    echo     "is_mandatory": false,
    echo     "message": "Nova versao disponivel com melhorias importantes!",
    echo     "signature": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    echo } > update_manifest.json
    echo Arquivo 'update_manifest.json' criado com sucesso.
)

echo.

REM Verifica se o arquivo README.md existe
if exist "README.md" (
    echo Arquivo 'README.md' ja existe.
) else (
    echo Copiando arquivo 'GITHUB_README.md' para 'README.md'...
    copy GITHUB_README.md README.md > nul
    echo Arquivo 'README.md' criado com sucesso.
)

echo.

echo ===================================================
echo Configuracao concluida com sucesso!
echo ===================================================
echo.
echo Proximos passos:
echo 1. Adicione os arquivos ao repositorio: git add .
echo 2. Faca o commit inicial: git commit -m "Configuracao inicial do repositorio de atualizacoes"
echo 3. Envie para o GitHub: git push -u origin main
echo 4. Crie uma release no GitHub com a tag v1.0.0 e faca upload do instalador
echo.

pause