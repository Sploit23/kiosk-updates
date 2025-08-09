let grupos = {};
let fotoSelecionada = null;
let variacoesAtuais = [];
let appVersion = "1.0.0";
let updateAvailable = false;

// Verifica se há atualizações disponíveis
async function verificarAtualizacoes() {
    try {
        const response = await fetch("/api/version");
        if (response.ok) {
            const versionInfo = await response.json();
            appVersion = versionInfo.version;
            
            // Atualiza a versão na interface
            const versionElement = document.getElementById("app-version");
            if (versionElement) {
                versionElement.textContent = `v${appVersion}`;
            }
            
            // Verifica se há atualizações disponíveis
            const updateResponse = await fetch("/api/check-update");
            if (updateResponse.ok) {
                const updateInfo = await updateResponse.json();
                
                if (updateInfo.status === "success" && updateInfo.has_update) {
                    updateAvailable = true;
                    mostrarNotificacaoAtualizacao(updateInfo);
                }
            }
        }
    } catch (error) {
        console.error("Erro ao verificar atualizações:", error);
    }
}

// Mostra notificação de atualização disponível
function mostrarNotificacaoAtualizacao(updateInfo) {
    const notificacao = document.createElement("div");
    notificacao.className = "update-notification";
    
    const titulo = document.createElement("h3");
    titulo.textContent = "Nova versão disponível!";
    
    const versao = document.createElement("p");
    versao.textContent = `Versão ${updateInfo.latest_version} disponível (atual: v${appVersion})`;
    
    const changelog = document.createElement("ul");
    if (updateInfo.changelog && updateInfo.changelog.length > 0) {
        updateInfo.changelog.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            changelog.appendChild(li);
        });
    }
    
    const fecharBtn = document.createElement("button");
    fecharBtn.className = "update-close";
    fecharBtn.textContent = "Fechar";
    fecharBtn.onclick = () => notificacao.remove();
    
    notificacao.appendChild(titulo);
    notificacao.appendChild(versao);
    notificacao.appendChild(changelog);
    notificacao.appendChild(fecharBtn);
    
    document.body.appendChild(notificacao);
}

// Carrega lista de imagens do servidor
async function carregarImagens() {
    const resp = await fetch("/api/images");
    if (!resp.ok) {
        document.getElementById("main").innerHTML = `<h2 class="loading">Erro ao carregar fotos.</h2>`;
        console.error("Erro ao carregar fotos:", await resp.json());
        return;
    }
    grupos = await resp.json();

    if (Object.keys(grupos).length === 0) {
        document.getElementById("main").innerHTML = `<h2 class="loading">Nenhuma foto encontrada para hoje.</h2>`;
        return;
    }

    const listaDiv = document.getElementById("lista-fotos");
    listaDiv.innerHTML = "";
    for (let num in grupos) {
        const primeira = grupos[num][0];
        const div = document.createElement("div");
        div.className = "foto-sidebar";

        const img = document.createElement("img");
        img.src = "/imagens/" + primeira;
        img.alt = `Foto ${num}`;
        img.onclick = () => selecionarFoto(num, div);

        const numeroDiv = document.createElement("div");
        numeroDiv.className = "foto-numero";
        numeroDiv.textContent = "ID " + num;

        div.appendChild(img);
        div.appendChild(numeroDiv);
        listaDiv.appendChild(div);
    }
    
    const primeiroId = Object.keys(grupos)[0];
    if (primeiroId) {
        selecionarFoto(primeiroId, document.querySelector('.foto-sidebar'));
    }
}

function selecionarFoto(num, element) {
    document.querySelectorAll('.foto-sidebar').forEach(el => el.classList.remove('selected'));
    if (element) {
        element.classList.add('selected');
    }

    fotoSelecionada = num;
    variacoesAtuais = grupos[num];
    mostrarFotoGrande(variacoesAtuais[0]);
    mostrarMiniaturas();
}

function mostrarFotoGrande(nome) {
    const fotoDiv = document.getElementById("foto-grande");
    fotoDiv.innerHTML = "";

    const img = document.createElement("img");
    img.id = "foto-grande-img";
    img.src = "/imagens/" + nome;

    // Importa o módulo de impressão
    import('./printer.js')
        .then(module => {
            window.printerService = module.printer;
        })
        .catch(error => {
            console.error("Erro ao carregar módulo de impressão:", error);
        });
    
    const btn = document.createElement("button");
    btn.id = "botao-imprimir";
    btn.textContent = "Imprimir " + nome.split("_")[0];
    btn.onclick = async () => {
        btn.disabled = true;
        btn.textContent = "Enviando...";
        
        try {
            // Se o serviço de impressão estiver disponível, usa a API
            if (window.printerService) {
                await window.printerService.printImage("/imagens/" + nome);
            } else {
                // Fallback para o método antigo
                const w = window.open("/imagens/" + nome);
                w.onload = () => {
                    w.print();
                };
            }
        } catch (error) {
            console.error("Erro ao imprimir:", error);
            alert("Erro ao imprimir: " + error.message);
        } finally {
            btn.disabled = false;
            btn.textContent = "Imprimir " + nome.split("_")[0];
        }
    };
    
    const titulo = document.createElement("h2");
    titulo.textContent = "Foto ID " + fotoSelecionada;

    fotoDiv.appendChild(titulo);
    fotoDiv.appendChild(img);
    fotoDiv.appendChild(btn);
}

function mostrarMiniaturas() {
    const miniDiv = document.getElementById("miniaturas");
    miniDiv.innerHTML = "";

    variacoesAtuais.forEach(nome => {
        const div = document.createElement("div");
        div.className = "miniatura";

        const img = document.createElement("img");
        img.src = "/imagens/" + nome;
        img.onclick = () => mostrarFotoGrande(nome);

        const nomeDiv = document.createElement("div");
        nomeDiv.className = "miniatura-nome";
        nomeDiv.textContent = nome.split("_")[0];

        div.appendChild(img);
        div.appendChild(nomeDiv);
        miniDiv.appendChild(div);
    });
}

const snowflakes = ['❄️', '❅', '❆', '🎄', '🎁', '⭐'];
function createSnowflake() {
    const snowflake = document.createElement('div');
    snowflake.innerHTML = snowflakes[Math.floor(Math.random() * snowflakes.length)];
    snowflake.className = 'snowflake';
    snowflake.style.left = `${Math.random() * 100}vw`;
    snowflake.style.animationDuration = `${Math.random() * 10 + 5}s`;
    snowflake.style.animationDelay = `${Math.random() * 5}s`;
    snowflake.style.opacity = Math.random();
    snowflake.style.fontSize = `${Math.random() * 1 + 0.5}em`;
    document.body.appendChild(snowflake);
}
setInterval(createSnowflake, 500);

// Adiciona informações de versão ao rodapé
function adicionarInfoVersao() {
    const footer = document.createElement("div");
    footer.className = "app-footer";
    
    const versionSpan = document.createElement("span");
    versionSpan.id = "app-version";
    versionSpan.textContent = `v${appVersion}`;
    
    footer.appendChild(versionSpan);
    document.body.appendChild(footer);
}

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', () => {
    carregarImagens();
    adicionarInfoVersao();
    verificarAtualizacoes();
    
    // Verifica atualizações a cada 30 minutos
    setInterval(verificarAtualizacoes, 30 * 60 * 1000);
});