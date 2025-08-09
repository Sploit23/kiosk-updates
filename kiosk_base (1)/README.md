# 📸 Kiosk de Seleção e Impressão de Fotos

## ✅ O que já temos implementado
- **Interface HTML+CSS+JS responsiva**.
- **Barra lateral (sidebar)** que exibe todas as fotos originais agrupadas pelo número da foto.
- **Área principal** que mostra:
  - Foto grande da variação selecionada.
  - Botão para imprimir via diálogo do Windows.
  - Miniaturas das 3 variações (10x15, 15x20, Bolas) com nome abaixo.
  - **Número da foto (ID)** abaixo das miniaturas.
- **Agrupamento automático** das imagens por ID da foto original.
- **Servidor Python (Flask)** que lista as imagens da pasta `imagens/` sem precisar editar código.
- **Compatível com tela cheia e touch screen**.

## 📂 Estrutura de Pastas
```
/projeto
   ├── server.py        # Servidor Flask
   ├── index.html       # Interface do kiosk
   ├── imagens/         # Pasta onde ficam as fotos processadas
```

## 🚀 Como rodar
1. Instalar dependências:
   ```bash
   pip install flask
   ```
2. Colocar as fotos processadas na pasta `imagens/` (nomes no formato `10x15_data_id.jpg`, `15x20_data_id.jpg`, `Bolas_data_id.jpg`).
3. Rodar o servidor:
   ```bash
   python server.py
   ```
4. Abrir no navegador:
   ```
   http://localhost:5000
   ```
5. Ativar **tela cheia (F11)**.

## 🔮 Melhorias planejadas
1. **Autoatualização** da lista de fotos sem recarregar a página.
2. **Zoom com toque** na foto grande.
3. **Botões de impressão grandes e coloridos** para facilitar o uso em tela touch.
4. **Filtro de busca por número da foto** para facilitar quando há muitas imagens.
5. **Opção de impressão automática** no tamanho correto, sem abrir o diálogo do Windows.
6. **Feedback visual** após enviar para impressão (ex.: mensagem "Foto enviada para impressão").
