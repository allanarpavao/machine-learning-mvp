// URL base da sua API Flask/FastAPI (Ajuste a porta conforme o backend)
const API_URL = 'http://localhost:5000/api/predict';

document.getElementById('predictionForm').addEventListener('submit', async function(event) {
    // Evita o recarregamento da página (comportamento SPA)
    event.preventDefault();

    const form = event.target;
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const resultSection = document.getElementById('resultSection');

    // 1. Coleta os dados do formulário
    const formData = new FormData(form);
    const dataPayload = Object.fromEntries(formData.entries());

    // Converte os valores para números (o modelo de ML geralmente exige formato numérico)
    for (let key in dataPayload) {
        dataPayload[key] = parseFloat(dataPayload[key]);
    }

    // 2. Altera estado da UI para "Carregando"
    submitBtn.disabled = true;
    btnText.textContent = 'Analisando...';
    btnLoader.classList.remove('hidden');
    resultSection.classList.add('hidden');

    try {
        // 3. Faz a requisição POST para o Back-end
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Necessário se houver validação de segurança/CORS configurada
                'Accept': 'application/json' 
            },
            body: JSON.stringify(dataPayload)
        });

        if (!response.ok) {
            throw new Error(`Erro na API: ${response.statusText}`);
        }

        const result = await response.json();
        
        // 4. Exibe o resultado na tela
        showResult(result.prediction); // Espera-se que a API retorne { "prediction": "Graduate" }

    } catch (error) {
        console.error('Erro ao realizar a predição:', error);
        alert('Falha ao conectar com o servidor. Verifique se a API está rodando.');
    } finally {
        // 5. Restaura o estado do botão
        submitBtn.disabled = false;
        btnText.textContent = 'Realizar Predição';
        btnLoader.classList.add('hidden');
    }
});

function showResult(predictionClass) {
    const resultSection = document.getElementById('resultSection');
    const badge = document.getElementById('predictionBadge');
    const message = document.getElementById('predictionMessage');

    // Limpa classes anteriores
    badge.className = 'badge';

    // Mapeia as classes do modelo para a UI
    // Os textos variam dependendo de como seu LabelEncoder foi treinado no Python
    if (predictionClass.toLowerCase() === 'graduate' || predictionClass === 1) {
        badge.textContent = 'Aprovado / Formado';
        badge.classList.add('graduate');
        message.textContent = 'Este aluno tem alta probabilidade de concluir o curso com sucesso.';
    } 
    else if (predictionClass.toLowerCase() === 'dropout' || predictionClass === 0) {
        badge.textContent = 'Risco de Evasão';
        badge.classList.add('dropout');
        message.textContent = 'Atenção: Este aluno apresenta alto risco de abandonar o curso. Sugerimos intervenção pedagógica.';
    } 
    else {
        badge.textContent = 'Matriculado (Regular)';
        badge.classList.add('enrolled');
        message.textContent = 'Aluno em progressão normal, requer acompanhamento padrão.';
    }

    // Exibe a seção com animação CSS
    resultSection.classList.remove('hidden');
    // Rola a tela suavemente para o resultado
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('resultSection').classList.add('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}