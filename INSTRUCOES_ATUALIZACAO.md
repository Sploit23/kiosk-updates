# Instruções para o Sistema de Atualização Automática

## Visão Geral

O sistema de atualização automática do Kiosk Photo permite que você distribua novas versões do aplicativo de forma simples e eficiente. O sistema utiliza o GitHub como servidor de atualizações, aproveitando seus recursos de hospedagem de arquivos e controle de versão.

## Configuração Inicial

### 1. Preparação do Repositório GitHub

1. Acesse o repositório já criado: https://github.com/Sploit23/kiosk-updates
2. Clone o repositório para sua máquina local:
   ```
   git clone https://github.com/Sploit23/kiosk-updates.git
   ```
3. Execute o script `setup_update_repo.bat` para configurar a estrutura básica do repositório:
   ```
   setup_update_repo.bat
   ```
4. Siga as instruções exibidas pelo script para adicionar os arquivos ao repositório e enviá-los para o GitHub.

### 2. Configuração do Aplicativo

O aplicativo já está configurado para usar o repositório GitHub como servidor de atualizações. Os arquivos relevantes são:

- `modules/updater.py`: Contém a lógica para verificar, baixar e aplicar atualizações.
- `version.json`: Contém informações sobre a versão atual do aplicativo.
- `static/app.js`: Contém o código para verificar atualizações e notificar o usuário.

## Fluxo de Trabalho para Lançar Atualizações

### 1. Desenvolvimento de Novas Funcionalidades

1. Desenvolva e teste as novas funcionalidades no código-fonte do aplicativo.
2. Atualize o número da versão no arquivo `version.json`.
3. Atualize o changelog no arquivo `version.json` com as mudanças realizadas.

### 2. Geração do Executável e Instalador

1. Execute o script `build_executable.py` para gerar o executável:
   ```
   python build_executable.py
   ```
2. Execute o Inno Setup para criar o instalador usando o script `installer_script.iss`.

Alternativamente, você pode usar o script `create_test_update.bat` para automatizar esse processo:
```
create_test_update.bat
```

### 3. Publicação da Atualização

1. Crie uma nova tag/release no GitHub (ex: v1.1.0).
2. Faça upload do instalador para a release.
3. Atualize o arquivo `update_manifest.json` com as informações da nova versão usando o script `publish_update.py`:
   ```
   python publish_update.py 1.1.0 caminho/para/instalador.exe --changelog "Nova funcionalidade" "Correção de bug"
   ```
4. Faça commit e push das alterações para o repositório:
   ```
   git add update_manifest.json
   git commit -m "Atualização do manifesto para versão 1.1.0"
   git push
   ```

### 4. Verificação

1. Teste o processo de atualização em uma instalação existente do aplicativo usando o script `test_update_system.py`:
   ```
   python test_update_system.py
   ```
2. Verifique se o aplicativo detecta a nova versão e oferece a opção de atualizar.
3. Confirme que o download e a instalação da atualização funcionam corretamente.

## Estrutura do Manifesto de Atualização

O arquivo `update_manifest.json` contém as seguintes informações:

```json
{
    "latest_version": "1.1.0",            // Número da versão mais recente
    "min_compatible_version": "1.0.0",    // Versão mínima compatível
    "download_url": "https://...",        // URL para download do instalador
    "changelog": [                        // Lista de mudanças
        "Nova funcionalidade",
        "Correção de bug"
    ],
    "release_date": "2023-12-20",         // Data de lançamento
    "is_mandatory": false,                // Se a atualização é obrigatória
    "message": "Nova versão disponível!", // Mensagem para o usuário
    "signature": "sha256:..."             // Hash SHA-256 do instalador
}
```

## Ferramentas Disponíveis

### Scripts de Automação

- `setup_update_repo.bat`: Configura a estrutura básica do repositório de atualizações.
- `create_test_update.bat`: Cria uma nova versão de teste do aplicativo.
- `publish_update.py`: Atualiza o manifesto de atualização com as informações da nova versão.
- `test_update_system.py`: Testa se o sistema de atualização está funcionando corretamente.

### Arquivos de Configuração

- `update_manifest.json`: Contém informações sobre a versão mais recente disponível.
- `version.json`: Contém informações sobre a versão atual do aplicativo.
- `GITHUB_README.md`: README para o repositório de atualizações no GitHub.

## Solução de Problemas

### O aplicativo não detecta atualizações

1. Verifique se o arquivo `update_manifest.json` está acessível no GitHub.
2. Confirme que a versão no manifesto é maior que a versão atual do aplicativo.
3. Verifique se a URL de atualização no arquivo `version.json` está correta.
4. Execute o script `test_update_system.py` para diagnosticar problemas.

### Erro ao baixar a atualização

1. Verifique se a URL de download no manifesto está correta.
2. Confirme que o instalador foi enviado para a release no GitHub.
3. Verifique se o usuário tem permissão para baixar arquivos da internet.

### Erro ao aplicar a atualização

1. Verifique se o instalador foi baixado corretamente.
2. Confirme que o usuário tem permissão para executar o instalador.
3. Verifique os logs do aplicativo para mais informações sobre o erro.

## Considerações de Segurança

- O sistema verifica o hash SHA-256 do instalador para garantir sua integridade.
- As atualizações são baixadas via HTTPS para garantir a segurança da transferência.
- O sistema verifica a compatibilidade da versão antes de aplicar a atualização.

## Suporte

Para dúvidas ou problemas relacionados ao sistema de atualização, entre em contato com o desenvolvedor ou abra uma issue no repositório do GitHub.