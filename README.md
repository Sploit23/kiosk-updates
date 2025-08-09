# Sistema de Visualização de Fotos com Impressão

Sistema web para visualização e impressão de fotos organizadas por data, com interface em modo quiosque.

## Estrutura do Projeto

```
├── config/                     # Arquivos de configuração
│   ├── settings.json          # Configurações principais
│   ├── themes.json            # Configurações de temas
│   ├── version.json           # Informações de versão
│   └── printer_settings.json  # Configurações da impressora
├── modules/                    # Módulos organizados
│   ├── printer/               # Módulo de impressão
│   │   ├── __init__.py
│   │   └── printer_config.py  # Configurações da impressora
│   └── updater/               # Módulo de atualizações
│       ├── __init__.py
│       └── update_manager.py  # Gerenciador de atualizações
├── static/                     # Arquivos estáticos
│   ├── css/                   # Folhas de estilo
│   │   └── core.css
│   ├── js/                    # Scripts JavaScript
│   │   ├── app.js             # Script principal
│   │   └── printer.js         # Script de impressão
│   └── assets/                # Recursos adicionais
│       └── themes/            # Temas da aplicação
│           └── christmas/
│               └── theme.js
├── templates/                  # Templates HTML
│   ├── index.html             # Página principal
│   └── config.html            # Página de configuração
├── server.py                   # Servidor Flask principal
├── start.bat                   # Script de inicialização
└── README.md                   # Documentação
```

## Funcionalidades

- **Visualização de Fotos**: Interface para navegar pelas fotos organizadas por data
- **Impressão**: Sistema de impressão integrado com configurações personalizáveis
- **Configuração**: Interface web para configurar pasta de imagens e impressora
- **Modo Quiosque**: Inicialização automática em tela cheia
- **Temas**: Sistema de temas personalizáveis
- **Atualizações**: Sistema de verificação e aplicação de atualizações

## Como Usar

1. Execute `start.bat` para iniciar o servidor e abrir o navegador
2. Configure a pasta de imagens através do botão de configuração (⚙️)
3. Navegue pelas fotos usando os controles da interface
4. Use os botões de impressão para imprimir as fotos selecionadas

## Configuração

### Pasta de Imagens
- Acesse a página de configuração através do ícone de engrenagem
- Selecione a pasta base onde estão organizadas as fotos por data
- As fotos devem estar organizadas em pastas com formato AAAAMMDD

### Impressora
- As configurações da impressora são gerenciadas pelo módulo `modules/printer/`
- Configurações são salvas em `config/printer_settings.json`

## Desenvolvimento

### Estrutura Modular
- **modules/printer/**: Gerencia todas as configurações e operações de impressão
- **modules/updater/**: Gerencia verificação e aplicação de atualizações
- **config/**: Centraliza todos os arquivos de configuração
- **static/**: Organiza recursos estáticos em subpastas específicas

### Tecnologias Utilizadas
- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Configuração**: JSON
- **Impressão**: JavaScript Print API

## Requisitos

- Python 3.7+
- Flask
- Requests (para verificação de atualizações)
- Navegador web moderno

## Roadmap para Versão Comercial

### 1. Melhorias na Experiência do Cliente

#### Interface do Usuário
- [ ] Simplificar a navegação com botões maiores para telas touch
- [ ] Adicionar feedback visual para ações (especialmente após impressão)
- [ ] Implementar modo guiado/tutorial para novos usuários
- [ ] Permitir ajustes básicos nas fotos (brilho/contraste)
- [ ] Adicionar filtros e molduras decorativas

#### Funcionalidades Comerciais
- [ ] Integrar sistema de pagamento (PIX, cartão)
- [ ] Exibir preços claramente para cada formato
- [ ] Implementar sistema de promoções e pacotes
- [ ] Adicionar contador de impressões para controle

### 2. Otimização Técnica

#### Empacotamento e Distribuição
- [ ] Converter para executável com PyInstaller
- [ ] Criar instalador profissional com configuração automática
- [ ] Implementar sistema de atualizações automáticas

#### Performance
- [ ] Otimizar carregamento de imagens (thumbnails, lazy loading)
- [ ] Implementar sistema de cache para acesso rápido
- [ ] Melhorar tempo de inicialização

#### Robustez
- [ ] Garantir funcionamento offline
- [ ] Implementar recuperação de erros
- [ ] Adicionar sistema de logs detalhados

### 3. Recursos Administrativos

#### Painel de Controle
- [ ] Criar dashboard administrativo protegido por senha
- [ ] Implementar relatórios de uso e faturamento
- [ ] Desenvolver sistema de gerenciamento remoto

#### Integração com Equipamentos
- [ ] Finalizar suporte a múltiplas impressoras
- [ ] Implementar calibração de cores
- [ ] Adicionar suporte para câmeras (opcional)

## Guia de Implementação (Curto Prazo)

### 1. Finalizar a Integração de Impressão

#### Passos:
1. Completar a integração entre o módulo `printer.py` e o frontend
2. Implementar fila de impressão no backend
3. Adicionar feedback visual durante o processo de impressão
4. Implementar tratamento de erros de impressão

#### Arquivos a modificar:
- `static/printer.js`: Conectar com a API do backend
- `modules/printer.py`: Finalizar implementação
- `server.py`: Adicionar endpoints para impressão
- `static/app.js`: Atualizar interface para mostrar status de impressão

### 2. Criar Executável com PyInstaller

#### Requisitos:
- Python 3.8+ instalado
- PyInstaller (`pip install pyinstaller`)
- Dependências do projeto instaladas

#### Passos:
1. Instalar PyInstaller: `pip install pyinstaller`
2. Criar arquivo spec personalizado
3. Compilar o executável
4. Testar em ambiente limpo

#### Exemplo de comando:
```
pyinstaller --onefile --windowed --icon=icon.ico --add-data "templates;templates" --add-data "static;static" server.py
```

### 3. Sistema de Atualização Automática (Implementado)

#### Arquitetura:
1. Servidor de atualizações via GitHub (https://github.com/Sploit23/kiosk-updates)
2. Arquivo de manifesto com versão atual e URLs (`update_manifest.json`)
3. Cliente de atualização no aplicativo (`modules/updater.py`)

#### Funcionamento:
1. O aplicativo verifica periodicamente o arquivo `update_manifest.json` no repositório GitHub
2. Se uma nova versão estiver disponível, o aplicativo notifica o usuário
3. Quando o usuário confirma, o aplicativo baixa o instalador da nova versão
4. Após o download, o aplicativo é fechado e o instalador é executado automaticamente

#### Lançando Atualizações:
1. Gerar o executável do aplicativo usando o script `build_executable.py`
2. Criar um instalador usando o script Inno Setup (`installer_script.iss`)
3. Criar uma nova release no GitHub e fazer upload do instalador
4. Atualizar o arquivo `update_manifest.json` com as informações da nova versão

## Estrutura do Projeto

```
/projeto
   ├── server.py        # Servidor Flask principal
   ├── settings.json    # Configurações do servidor
   ├── themes.json      # Configurações de temas
   ├── version.json     # Informações de versão (a ser criado)
   ├── modules/         # Módulos Python
   │   └── printer.py   # Módulo de impressão
   ├── static/          # Arquivos estáticos
   │   ├── app.js       # Lógica principal do frontend
   │   ├── core.css     # Estilos CSS
   │   └── printer.js   # Lógica de impressão do frontend
   ├── templates/       # Templates HTML
   │   └── index.html   # Interface principal
   └── imagens/         # Pasta de imagens
       └── [data]/      # Subpastas organizadas por data
```

## Requisitos

- Python 3.8+
- Flask
- Pillow (PIL)
- win32print (para Windows)
- PyInstaller (para criar executável)

## Como Executar (Desenvolvimento)

1. Instalar dependências:
   ```
   pip install flask pillow pywin32
   ```

2. Executar o servidor:
   ```
   python server.py
   ```

3. Acessar no navegador:
   ```
   http://localhost:5000
   ```

## Licenciamento e Distribuição

- Definir modelo de licenciamento (por quiosque, por tempo, etc.)
- Estabelecer termos de uso e política de privacidade
- Criar documentação para usuário final

## Suporte e Contato

- Adicionar informações de suporte técnico
- Estabelecer canais de comunicação para feedback

---

© 2023 Quiosque de Fotos. Todos os direitos reservados.