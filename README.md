# SGA Analytics — Sistema de Predição de Evasão Escolar

Aplicação fullstack para predição da situação acadêmica de estudantes do ensino superior — **Graduate**, **Enrolled** ou **Dropout** — a partir de variáveis socioeconômicas, demográficas e de desempenho acadêmico.

O sistema integra um modelo de machine learning, uma API REST documentada via OpenAPI e um frontend que serve como painel para a secretaria acadêmica realizar consultas em tempo real. O objetivo aplicado é identificar precocemente estudantes em risco de evasão, permitindo intervenções preventivas direcionadas.

---

## Arquitetura

```
┌─────────────────────┐        HTTP/JSON         ┌─────────────────────────┐
│      Frontend       │  ──────────────────────▶ │           API           │
│  (HTML/CSS/JS puro) │                          │ (Flask + OpenAPI3 + CORS)│
│                     │ ◀──────────────────────  │                         │
└─────────────────────┘     situacao_academica   └────────────┬────────────┘
                                                              │
                                              ┌───────────────┼───────────────┐
                                              │               │               │
                                              ▼               ▼               ▼
                                       ┌────────────┐  ┌────────────┐  ┌────────────┐
                                       │  Pipeline  │  │  SQLite    │  │  Pydantic  │
                                       │  ML (.pkl) │  │  (SQLAlc.) │  │  schemas   │
                                       └────────────┘  └────────────┘  └────────────┘
```

O backend serve a aplicação inteira: as rotas `/` e `/<filename>` entregam os arquivos do frontend, e as rotas `/estudantes/*` expõem a API de predição. Isso elimina problemas de CORS em produção e simplifica o deploy.

---

## Stack Técnica

### Machine Learning
- **Python 3.11** — linguagem base
- **Pandas / NumPy** — manipulação de dados
- **Scikit-learn** — pipeline, validação cruzada, GridSearch, métricas
- **Imbalanced-learn (SMOTE)** — balanceamento de classes
- **Jupyter Notebook** — experimentação e treinamento
- **Pickle** — serialização do pipeline treinado

### Backend (API)
- **Flask** — microframework HTTP
- **Flask-OpenAPI3** — documentação automática (Swagger UI) e validação via Pydantic
- **Flask-CORS** — liberação de origem cruzada para desenvolvimento
- **SQLAlchemy 2.x** — ORM com mapeamento tipado (`Mapped[...]`)
- **SQLAlchemy-Utils** — utilidades de criação de banco
- **Pydantic v2** — validação de entrada e serialização de saída
- **SQLite** — persistência local

### Frontend
- **HTML5 / CSS3** — estrutura e estilo
- **JavaScript (vanilla)** — consumo da API via `fetch` (SPA leve, sem framework)
- **Inter (Google Fonts)** — tipografia

### Testes
- **Pytest** — testes do modelo de ML

---

## Estrutura do Projeto

```
machine-learning-mvp/
├── api/                              # Backend Flask
│   ├── app.py                        # Bootstrap da aplicação (registra blueprints, serve frontend)
│   ├── routes/
│   │   └── estudantes.py             # Endpoints de predição/listagem/exclusão
│   ├── models/
│   │   ├── base.py                   # Base declarativa do SQLAlchemy
│   │   ├── estudantes.py             # Modelo Estudante (36 atributos)
│   │   └── machine_learning.py       # Pipeline, Preprocessador e Avaliador
│   ├── schemas/
│   │   └── estudantes.py             # Schemas Pydantic de entrada/saída
│   ├── database/
│   │   └── db.sqlite3                # Banco local (gerado em runtime)
│   ├── MachineLearning/
│   │   ├── data/                     # Dataset original (UCI)
│   │   ├── models/
│   │   │   └── students_pipeline.pkl # Pipeline serializado
│   │   └── students-*.ipynb          # Notebooks de estudo, treino e teste
│   └── test_modelos.py               # Testes do pipeline serializado
├── front/                            # Frontend estático
│   ├── index.html                    # Formulário e resultado da predição
│   ├── scripts.js                    # Lógica de submit/fetch/render
│   └── styles.css                    # Tema visual (paleta acadêmica)
├── requirements.txt                  # Dependências Python
└── README.md
```

---

## Como Executar

### 1. Pré-requisitos

- Python 3.11
- `pip` disponível
- (Opcional) `virtualenv` ou `venv` para isolar o ambiente

### 2. Instalação

```bash
git clone https://github.com/allanapavao/machine-learning-mvp.git
cd machine-learning-mvp

python3 -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

### 3. Subir a aplicação

```bash
cd api
python app.py
```

A aplicação fica disponível em:

| Recurso | URL |
|---|---|
| Frontend | http://localhost:8000/ |
| Documentação OpenAPI (Swagger) | http://localhost:8000/openapi |
| Atalho para docs | http://localhost:8000/docs |
| Endpoint de predição | http://localhost:8000/estudantes/criar |

O banco SQLite e o diretório `database/` são criados automaticamente no primeiro start.

### 4. Rodar testes

```bash
cd api
python -m pytest -v test_modelos.py
```

Os testes verificam o pipeline serializado contra o dataset original, assegurando acurácia ≥ 0.75, recall ≥ 0.75 e F1 ≥ 0.70. Há também um teste negativo com `DummyClassifier` para validar que modelos triviais não passam pelos thresholds.

---

## API — Endpoints

Todas as rotas vivem sob o prefixo `/estudantes` e são documentadas automaticamente pelo Flask-OpenAPI3.

### `POST /estudantes/criar`

Recebe os 33 atributos de um estudante, executa a predição e persiste o registro com a `situacao_academica` retornada pelo modelo.

**Request body** (JSON, validado por `EstudanteSchema`):

```json
{
  "father_qualification": 1,
  "mother_qualification": 1,
  "father_occupation": 1,
  "mother_occupation": 1,
  "education_special_needs": 0,
  "debtor": 0,
  "tuition_fees_up_to_date": 1,
  "scholarship_holder": 0,
  "marital_status": 1,
  "nationality": 1,
  "displaced": 1,
  "gender": 0,
  "age_at_enrollment": 19,
  "international": 0,
  "application_mode": 1,
  "application_order": 4,
  "course": 1,
  "daytime_evening_attendance": 1,
  "previous_qualification": 1,
  "previous_qualification_grade": 95.0,
  "admission_grade": 95.0,
  "curricular_units_1st_sem_credited": 0,
  "curricular_units_1st_sem_enrolled": 6,
  "curricular_units_1st_sem_evaluations": 8,
  "curricular_units_1st_sem_approved": 5,
  "curricular_units_1st_sem_grade": 14.333,
  "curricular_units_1st_sem_without_evaluations": 0,
  "curricular_units_2nd_sem_credited": 0,
  "curricular_units_2nd_sem_enrolled": 6,
  "curricular_units_2nd_sem_evaluations": 7,
  "curricular_units_2nd_sem_approved": 5,
  "curricular_units_2nd_sem_grade": 13.500,
  "curricular_units_2nd_sem_without_evaluations": 0
}
```

**Response** `201 Created`:

```json
{
  "matricula": 1,
  "situacao_academica": "Graduate"
}
```

### `GET /estudantes/listar`

Lista todos os estudantes persistidos. Retorna array vazio quando o banco está vazio.

### `DELETE /estudantes/?id_estudante=<int>`

Remove o estudante pela matrícula. Retorna 404 se o registro não existir.

---

## Fluxo Fullstack — Da entrada ao resultado

1. O usuário preenche o formulário em [front/index.html](front/index.html) com os 33 atributos do estudante. Há um botão **Preencher Dados Teste** que popula o formulário com valores válidos do schema.
2. O [scripts.js](front/scripts.js) intercepta o submit, converte os campos para `float` e envia um `POST` JSON para `/estudantes/criar`.
3. A rota [estudantes.py](api/routes/estudantes.py) valida o payload via `EstudanteSchema` (Pydantic).
4. O `Preprocessador` ordena as colunas conforme o `feature_names_in_` do pipeline serializado, evitando reordenação silenciosa.
5. O `Pipeline` carrega o `.pkl` e executa `predict`, retornando `Graduate`, `Enrolled` ou `Dropout`.
6. O `Estudante` é persistido no SQLite com matrícula gerada por `autoincrement`, e o resultado retorna ao frontend.
7. O frontend renderiza um badge colorido (verde/amarelo/vermelho) e uma mensagem direcionada à secretaria acadêmica.

---

## Modelo de ML — Raciocínio Técnico

### Diagnóstico inicial: desequilíbrio de classes

O primeiro passo antes de qualquer modelagem foi entender a distribuição das classes-alvo. O dataset apresenta desequilíbrio entre Graduate, Enrolled e Dropout e foi importante entender como isso afetaria o treinamento do modelo.

Com classes desbalanceadas, **acurácia é uma métrica enganosa**: um modelo que sempre prevê a classe majoritária pode atingir alta acurácia sem aprender nada útil. Por isso, a métrica de avaliação escolhida foi o **F1-score ponderado** (`f1_weighted`), que equilibra precisão e recall considerando o peso de cada classe.

### Prevenção de data leakage com Pipeline

Toda a lógica de pré-processamento — escalonamento e balanceamento — foi encapsulada dentro de um `Pipeline` do Scikit-learn (e `ImbPipeline` do Imbalanced-learn quando necessário). Isso garante que operações como `StandardScaler` e `SMOTE` sejam aplicadas **dentro de cada fold da validação cruzada**. Aplicar o scaler no dataset completo antes do split é um erro clássico que contamina o conjunto de validação com informações do treino — o pipeline elimina esse risco estruturalmente.

### Validação cruzada estratificada

A validação cruzada foi feita com `StratifiedKFold` com 10 partições. A estratificação é essencial aqui: ela garante que a proporção das classes originais seja mantida em cada fold. Usar `KFold` simples em dados desbalanceados pode resultar em folds onde uma classe minoritária está sub ou super-representada, tornando a avaliação instável.

### Comparação sistemática de algoritmos

Antes de comprometer recursos com otimização, seis algoritmos foram comparados em condições equivalentes:

| Algoritmo | Sigla |
|---|---|
| Regressão Logística | LR |
| K-Nearest Neighbors | KNN |
| Árvore de Decisão | CART |
| Naive Bayes | NB |
| Support Vector Machine | SVM |
| Gradient Boosting | GB |

Cada modelo foi testado em quatro configurações: dados originais, com padronização (`StandardScaler`), com normalização (`MinMaxScaler`) e com SMOTE em cada uma dessas variantes. O objetivo foi separar os efeitos do pré-processamento do efeito do algoritmo em si antes de decidir o que otimizar.

### Por que SMOTE?

O desequilíbrio entre as classes pode induzir viés no treinamento: classificadores tendem a favorecer a classe majoritária, sacrificando recall nas classes minoritárias. O **SMOTE (Synthetic Minority Oversampling Technique)** gera amostras sintéticas para as classes sub-representadas via interpolação entre instâncias reais existentes — diferente do oversampling simples por repetição, que não adiciona informação nova.

O SMOTE foi aplicado **dentro do pipeline**, garantindo que as amostras sintéticas sejam geradas apenas com base nos dados de treino de cada fold.

### Otimização de hiperparâmetros

Com os melhores candidatos identificados, o **GridSearchCV** foi aplicado para busca exaustiva dos hiperparâmetros mais relevantes de cada modelo. O critério de avaliação continuou sendo `f1_weighted`, com validação cruzada de 5 folds.

### Resultado e critério de seleção

Os três modelos com melhor desempenho após otimização foram:

| Modelo | F1-score (CV) | Configuração |
|---|---|---|
| GB-norm+smote | 0.770 | learning_rate=0.2, max_depth=3, n_estimators=100 |
| GB-padr+smote | 0.767 | learning_rate=0.1, max_depth=7, n_estimators=200 |
| SVM-padr+smote | 0.761 | kernel=rbf, C=100, gamma=0.001 |

O critério de seleção final levou em consideraçao o contexto do problema. O custo de não identificar um aluno em risco de evasão é maior do que classificar erroneamente um aluno matriculado, por isso o **recall da classe Dropout** foi o fator decisivo.

O modelo **GB-norm+smote** foi selecionado por apresentar o melhor equilíbrio entre F1-score geral e recall na classe Dropout. O desempenho inferior na classe Enrolled foi considerado aceitável: alunos ainda matriculados têm um perfil naturalmente ambíguo, pois eventualmente migrarão para Graduate ou Dropout — o modelo tem dificuldade estrutural com essa sobreposição, o que é esperado e documentado.

**Stack do modelo final:**

```
MinMaxScaler → SMOTE → GradientBoostingClassifier(learning_rate=0.2, max_depth=3, n_estimators=100)
```

---

## Fonte dos Dados

O dataset utilizado é público e mantido pela UCI Machine Learning Repository, contendo dados de estudantes de diversas universidades portuguesas. Cada registro representa um estudante com 36 atributos coletados em diferentes momentos do curso, incluindo situação socioeconômica familiar, desempenho no primeiro e segundo semestre, situação do débito de propinas e dados macroeconômicos do país.

Fonte: [UCI — Predict Students' Dropout and Academic Success](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)

> As variáveis macroeconômicas (`Unemployment rate`, `Inflation rate`, `GDP`) foram removidas do dataset de treinamento por não serem controláveis nem coletáveis no fluxo da aplicação.

---

## Decisões de Design (Fullstack)

**Frontend e backend no mesmo servidor.** O Flask serve os arquivos estáticos de `front/` diretamente via rota catch-all. Isso evita configuração de CORS em produção e simplifica o deploy (um único processo, uma única porta).

**Schemas Pydantic em uma única fonte de verdade.** O `EstudanteSchema` define defaults. Ele é usado simultaneamente para validação da entrada na API e para gerar a documentação OpenAPI — não há divergência entre a doc e o código.

**Ordenação explícita de features.** O `Preprocessador` extrai `feature_names_in_` do pipeline serializado e reordena o `DataFrame` antes da inferência. Isso protege contra mudanças silenciosas na ordem dos campos no frontend ou no schema.

**Pipeline serializado, não modelo isolado.** O `.pkl` contém todo o pipeline (scaler → SMOTE → classificador). Em produção, isso significa que o pré-processamento aplicado em treino é exatamente o mesmo aplicado em inferência — sem possibilidade de drift entre as duas etapas.

**Sessões com `scoped_session`.** A sessão do SQLAlchemy é por thread, e cada handler chama `Session.remove()` no `finally` para evitar vazamento de conexões.
