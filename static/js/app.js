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
    // Mostra loading com animação
    const mainDiv = document.getElementById("main");
    const originalContent = mainDiv.innerHTML;
    mainDiv.innerHTML = '<div class="loading-spinner"><div class="spinner"></div><p>Carregando fotos...</p></div>';
    
    try {
        const resp = await fetch("/api/images");
        if (!resp.ok) {
            const erro = await resp.json();
            console.error("Erro ao carregar fotos:", erro);
            
            let mensagemErro = `<div class="error-container">`;
            mensagemErro += `<h2 class="loading">Erro ao carregar fotos</h2>`;
            mensagemErro += `<p class="error-message">${erro.erro || 'Erro desconhecido'}</p>`;
            
            if (erro.solucao) {
                mensagemErro += `<p class="solution-message">${erro.solucao}</p>`;
            }
            
            mensagemErro += `<button class="config-button" onclick="window.location.href='/config'">Ir para Configurações</button>`;
            mensagemErro += `</div>`;
            
            mainDiv.innerHTML = mensagemErro;
            
            // Animação de entrada do erro
            setTimeout(() => {
                const errorContainer = document.querySelector('.error-container');
                if (errorContainer) {
                    errorContainer.style.opacity = '1';
                    errorContainer.style.transform = 'translateY(0)';
                }
            }, 100);
            
            return;
        }
        
        grupos = await resp.json();

        if (Object.keys(grupos).length === 0) {
            let mensagem = `<h2 class="loading">Nenhuma foto encontrada para hoje</h2>`;
            mensagem += `<p class="info-message">Verifique se as fotos foram copiadas para a pasta correta.</p>`;
            mensagem += `<button class="config-button" onclick="window.location.href='/config'">Ir para Configurações</button>`;
            
            document.getElementById("main").innerHTML = mensagem;
            return;
        }
        
        // Restaura o conteúdo original do main quando há fotos
        mainDiv.innerHTML = originalContent;
    } catch (error) {
        console.error("Erro ao processar requisição:", error);
        document.getElementById("main").innerHTML = `
            <h2 class="loading">Erro ao conectar com o servidor</h2>
            <p class="error-message">Verifique se o servidor está em execução.</p>
            <button class="config-button" onclick="window.location.href='/config'">Ir para Configurações</button>
        `;
        return;
    }

    const listaDiv = document.getElementById("lista-fotos");
    listaDiv.innerHTML = "";
    
    let index = 0;
    for (let num in grupos) {
        const primeira = grupos[num][0];
        const div = document.createElement("div");
        div.className = "foto-sidebar";
        
        // Animação de entrada escalonada
        div.style.opacity = '0';
        div.style.transform = 'translateX(-30px)';
        
        setTimeout(() => {
            div.style.opacity = '1';
            div.style.transform = 'translateX(0)';
        }, 100 + (index * 100));

        const img = document.createElement("img");
        img.src = "/imagens/" + primeira;
        img.alt = `Foto ${num}`;
        
        // Adiciona loading state para imagens
        img.style.opacity = '0';
        img.onload = () => {
            setTimeout(() => {
                img.style.opacity = '1';
            }, 200);
        };
        
        img.onclick = () => selecionarFoto(num, div);

        const numeroDiv = document.createElement("div");
        numeroDiv.className = "foto-numero";
        numeroDiv.textContent = "ID " + num;

        div.appendChild(img);
        div.appendChild(numeroDiv);
        listaDiv.appendChild(div);
        
        index++;
    }
    
    const primeiroId = Object.keys(grupos)[0];
    if (primeiroId) {
        selecionarFoto(primeiroId, document.querySelector('.foto-sidebar'));
    }
}

function selecionarFoto(num, element) {
    // Remove seleção anterior com animação
    document.querySelectorAll('.foto-sidebar').forEach(el => {
        el.classList.remove('selected');
        el.style.transform = 'scale(1)';
    });
    
    if (element) {
        element.classList.add('selected');
        // Adiciona efeito de seleção
        element.style.transform = 'scale(1.05) translateY(-5px)';
    }

    fotoSelecionada = num;
    variacoesAtuais = grupos[num];
    
    // Adiciona fade out antes de trocar a imagem
    const fotoGrande = document.getElementById('foto-grande-img');
    if (fotoGrande) {
        fotoGrande.style.opacity = '0';
        fotoGrande.style.transform = 'scale(0.95)';
        
        setTimeout(() => {
            mostrarFotoGrande(variacoesAtuais[0]);
            mostrarMiniaturas();
        }, 200);
    } else {
        mostrarFotoGrande(variacoesAtuais[0]);
        mostrarMiniaturas();
    }
}

function mostrarFotoGrande(nome) {
    const fotoDiv = document.getElementById("foto-grande");
    if (!fotoDiv) {
        console.error('Elemento foto-grande não encontrado');
        return;
    }
    fotoDiv.innerHTML = "";

    const img = document.createElement("img");
    img.id = "foto-grande-img";
    img.src = "/imagens/" + nome;
    
    // Adiciona loading state
    img.style.opacity = '0';
    img.style.transform = 'scale(0.9)';
    
    // Animação de entrada quando a imagem carregar
    img.onload = () => {
        setTimeout(() => {
            img.style.opacity = '1';
            img.style.transform = 'scale(1)';
        }, 100);
    };

    // Carrega o serviço de impressão
    if (typeof PrinterService !== 'undefined') {
        if (!window.printerService) {
            window.printerService = new PrinterService();
        }
    } else {
        console.warn("Serviço de impressão não disponível");
    }
    
    const btn = document.createElement("button");
    btn.id = "botao-imprimir";
    btn.textContent = "Imprimir " + nome.split("_")[0];
    btn.style.opacity = '0';
    btn.style.transform = 'translateY(20px)';
    
    // Animação de entrada do botão
    setTimeout(() => {
        btn.style.opacity = '1';
        btn.style.transform = 'translateY(0)';
    }, 300);
    
    btn.onclick = async () => {
        // Efeito visual de clique
        btn.style.transform = 'scale(0.95)';
        setTimeout(() => {
            btn.style.transform = 'scale(1)';
        }, 150);
        
        btn.disabled = true;
        btn.textContent = "Enviando...";
        btn.classList.add('loading');
        
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
            
            // Feedback visual de sucesso
            btn.style.background = 'linear-gradient(135deg, #28a745, #20c997)';
            btn.textContent = "Enviado!";
            
            setTimeout(() => {
                btn.style.background = '';
                btn.textContent = "Imprimir " + nome.split("_")[0];
            }, 2000);
            
        } catch (error) {
            console.error("Erro ao imprimir:", error);
            
            // Feedback visual de erro
            btn.style.background = 'linear-gradient(135deg, #dc3545, #c82333)';
            btn.textContent = "Erro!";
            
            setTimeout(() => {
                btn.style.background = '';
                btn.textContent = "Imprimir " + nome.split("_")[0];
            }, 2000);
            
            alert("Erro ao imprimir: " + error.message);
        } finally {
            btn.disabled = false;
            btn.classList.remove('loading');
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
    if (!miniDiv) {
        console.error('Elemento miniaturas não encontrado');
        return;
    }
    miniDiv.innerHTML = "";

    variacoesAtuais.forEach((nome, index) => {
        const div = document.createElement("div");
        div.className = "miniatura";
        
        // Animação de entrada escalonada
        div.style.opacity = '0';
        div.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            div.style.opacity = '1';
            div.style.transform = 'translateY(0)';
        }, 100 + (index * 50));

        const img = document.createElement("img");
        img.src = "/imagens/" + nome;
        
        // Adiciona efeito hover e clique
        img.onclick = () => {
            // Efeito de clique
            div.style.transform = 'scale(0.95)';
            setTimeout(() => {
                div.style.transform = 'scale(1)';
                mostrarFotoGrande(nome);
            }, 100);
        };
        
        // Efeitos hover
        div.addEventListener('mouseenter', () => {
            div.style.transform = 'translateY(-5px) scale(1.05)';
        });
        
        div.addEventListener('mouseleave', () => {
            div.style.transform = 'translateY(0) scale(1)';
        });

        const nomeDiv = document.createElement("div");
        nomeDiv.className = "miniatura-nome";
        nomeDiv.textContent = nome.split("_")[0];

        div.appendChild(img);
        div.appendChild(nomeDiv);
        miniDiv.appendChild(div);
    });
}

// Animações de flocos de neve removidas para melhor visualização das imagens

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