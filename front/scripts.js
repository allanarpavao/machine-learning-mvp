// URL base da sua API Flask/FastAPI (Ajuste a porta conforme o backend)
const API_URL = 'http://localhost:8000/estudantes/criar';

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
        
        showResult(result.situacao_academica); // Espera-se que a API retorne { "situacao_academica": "Graduate" }

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
    if (predictionClass.toLowerCase() === 'graduate' || predictionClass === 1) {
        badge.textContent = 'Formado';
        badge.classList.add('graduate');
        message.textContent = 'Este aluno tem alta probabilidade de concluir o curso com sucesso.';
    } 
    else if (predictionClass.toLowerCase() === 'dropout' || predictionClass === 0) {
        badge.textContent = 'Risco de Evasão';
        badge.classList.add('dropout');
        message.textContent = 'Atenção: Este aluno apresenta alto risco de abandonar o curso. Sugerimos intervenção pedagógica.';
    } 
    else {
        badge.textContent = 'Em Curso';
        badge.classList.add('enrolled');
        message.textContent = 'Aluno em progressão normal, requer acompanhamento padrão.';
    }

    resultSection.classList.remove('hidden');
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('resultSection').classList.add('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Preencher com dados de teste
const dadosPadraoSchema = {
    father_qualification: 1,
    mother_qualification: 1,
    father_occupation: 1,
    mother_occupation: 1,
    education_special_needs: 0,
    debtor: 0,
    tuition_fees_up_to_date: 1,
    scholarship_holder: 0,
    marital_status: 1,
    nationality: 1,
    displaced: 1,
    gender: 0,
    age_at_enrollment: 19,
    international: 0,
    application_mode: 1,
    application_order: 4,
    course: 1,
    daytime_evening_attendance: 1,
    previous_qualification: 1,
    previous_qualification_grade: 95.0,
    admission_grade: 95.0,
    curricular_units_1st_sem_credited: 0,
    curricular_units_1st_sem_enrolled: 6,
    curricular_units_1st_sem_evaluations: 8,
    curricular_units_1st_sem_approved: 5,
    curricular_units_1st_sem_grade: 14.333,
    curricular_units_1st_sem_without_evaluations: 0,
    curricular_units_2nd_sem_credited: 0,
    curricular_units_2nd_sem_enrolled: 6,
    curricular_units_2nd_sem_evaluations: 7,
    curricular_units_2nd_sem_approved: 5,
    curricular_units_2nd_sem_grade: 13.500,
    curricular_units_2nd_sem_without_evaluations: 0
};

function preencherDadosTeste() {
    for (const [chave, valor] of Object.entries(dadosPadraoSchema)) {
        const input = document.getElementById(chave);
        
        if (input) {
            input.value = valor;
        } else {
            console.warn(`Aviso: Input com id '${chave}' não foi encontrado no HTML.`);
        }
    }
}
