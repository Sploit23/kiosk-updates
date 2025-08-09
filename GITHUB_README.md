# Kiosk Photo - Sistema de Atualizações

Este repositório contém os arquivos necessários para o sistema de atualização automática do aplicativo Kiosk Photo.

## Estrutura do Repositório

- `update_manifest.json`: Arquivo principal que contém informações sobre a versão mais recente disponível.
- `releases/`: Diretório que contém os arquivos de instalação para cada versão (opcional).

## Como Funciona o Sistema de Atualização

1. O aplicativo Kiosk Photo verifica periodicamente o arquivo `update_manifest.json` neste repositório.
2. Se uma nova versão estiver disponível, o aplicativo notifica o usuário e oferece a opção de atualizar.
3. Quando o usuário confirma, o aplicativo baixa o instalador da nova versão a partir da URL especificada no manifesto.
4. Após o download, o aplicativo é fechado e o instalador é executado automaticamente.

## Lançando uma Nova Versão

Para lançar uma nova versão do aplicativo:

1. Gere o executável do aplicativo usando o script `build_executable.py`.
2. Crie um instalador usando o script Inno Setup (`installer_script.iss`).
3. Crie uma nova release no GitHub e faça upload do instalador.
4. Atualize o arquivo `update_manifest.json` com as informações da nova versão:
   - `latest_version`: Número da nova versão (ex: "1.1.0")
   - `min_compatible_version`: Versão mínima compatível
   - `download_url`: URL para download do instalador
   - `changelog`: Lista de mudanças na nova versão
   - `release_date`: Data de lançamento
   - `is_mandatory`: Se a atualização é obrigatória
   - `message`: Mensagem a ser exibida para o usuário

## Exemplo de Manifesto

```json
{
    "latest_version": "1.1.0",
    "min_compatible_version": "1.0.0",
    "download_url": "https://github.com/Sploit23/kiosk-updates/releases/download/v1.1.0/kiosk_photo_1.1.0.exe",
    "changelog": [
        "Novos recursos adicionados",
        "Correções de bugs",
        "Melhorias de desempenho"
    ],
    "release_date": "2023-12-20",
    "is_mandatory": false,
    "message": "Nova versão disponível com melhorias importantes!",
    "signature": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

## Fluxo de Trabalho para Atualizações

1. **Desenvolvimento de Novas Funcionalidades**
   - Desenvolva e teste as novas funcionalidades no repositório principal do aplicativo
   - Atualize o número da versão no arquivo `version.json`

2. **Geração do Executável e Instalador**
   - Execute o script `build_executable.py` para gerar o executável
   - Execute o Inno Setup para criar o instalador

3. **Publicação da Atualização**
   - Crie uma nova tag/release no GitHub (ex: v1.1.0)
   - Faça upload do instalador para a release
   - Atualize o arquivo `update_manifest.json` com as informações da nova versão
   - Faça commit e push das alterações para o repositório

4. **Verificação**
   - Teste o processo de atualização em uma instalação existente do aplicativo

## Suporte

Para dúvidas ou problemas relacionados ao sistema de atualização, abra uma issue neste repositório.