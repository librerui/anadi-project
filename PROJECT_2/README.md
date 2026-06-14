# Análise de Desempenho de Técnicas de Aprendizagem Automática: Viabilidade de VE na Rede de Distribuição

> Modelação preditiva e análise de desempenho de algoritmos de Machine Learning para a instalação de carregadores de veículos elétricos (VE) nos Postos de Transformação de Distribuição (PTD) da e-REDES.

## Contexto

Este projeto foi desenvolvido no âmbito da unidade curricular de **Análise de Dados em Informática** (ANADI) do curso de Engenharia Informática do ISEP (ano letivo 2025/2026).

Sendo a segunda iteração do projeto (Trabalho Prático 2), o estudo evolui da visão agregada por concelho para uma análise granular ao nível do Posto de Transformação de Distribuição (PTD). O objetivo centra-se na aplicação de técnicas de Aprendizagem Automática (Regressão e Classificação) para estimar a capacidade remanescente resultante da modernização da Iluminação Pública (transição para tecnologia LED) e avaliar de forma preditiva a estabilidade energética de cada posto.

## Metodologia

A análise segue detalhadamente o pipeline de ML:

1. **Pré-Processamento de Dados**: Feature selection rigorosa, tratamento de valores omissos, normalização (standardização), One-Hot/Label Encoding e discretização da variável alvo (`Util_Decimal`) gerando três níveis de classificação balanceada em `utilizRede` (baixo, médio e alto).
2. **Regressão**: Estimação da variável dependente contínua `PFolga_PTD` (Folga da Rede) recorrendo aos modelos: Regressão Linear Múltipla, Árvores de Regressão, SV Regressor (LinearSVR) e Redes Neuronais (MLPRegressor).
3. **Classificação**: Previsão de cenários da utilização (`utilizRede`), aplicando Árvores de Decisão, Redes Neuronais (MLPClassifier), Classificador SVM (LinearSVC) e K-Nearest Neighbors (KNN).
4. **Avaliação de Desempenho**: Estratégias de K-Fold Cross-Validation, otimização de Hiperparâmetros de base, Curvas de Loss, verificação da robustez na Curva de Aprendizagem (sobre/sub-ajustamento) e Feature Importance com relevância linear e não linear.
5. **Inferência Estatística**: Verificação da normalidade dos erros (Shapiro-Wilk) seguida do T-Test Pareado ou do teste não paramétrico Wilcoxon Signed-Rank para provar a validade temporal e prática dos melhores modelos de cada tipo metodológico.

## [Artigo científico](./article/conference_101719.pdf)

## Instalação e Execução

### Requisitos
- Python
- make (opcional, aplicável via repositório global)

### Setup
A partir da raiz do projeto, instale virtualmente as dependências (já partilhadas com o Projeto 1):
```bash
make venv
source .venv/bin/activate
```

**(Nota: É esperado que os dados de treino formados e preenchidos constem no diretório `/PROJECT_2/data/PTD_level_dataset.xlsx`. Os perfis de simulação de treino JSON encontram-se em `/PROJECT_2/profiles/`.)*

### Executar a Modelagem (Notebooks)
Para navegar pelos treinos, validações e previsões persistidas dos relatórios do classificador/regressor:

```bash
cd PROJECT_2
jupyter notebook main.ipynb
```

Através da diretoria, poderá invocar o *pipeline* ou avaliar os perfis gravados localmente em `results/` e referenciar através do notebook acessório `compare.ipynb`.

### Executar o Dashboard
```bash
make dashboard
```

O dashboard abre em `http://localhost:8501` e inclui as páginas:

| Página | Conteúdo |
|---|---|
| Principal | Painel com inputs para visualizar o resultado dos modelos |

## Fontes de Dados

| Dataset | Fonte | Descrição |
|---|---|---|
| `PTD_level_dataset.xlsx` | [e-REDES Open Data](https://e-redes.opendatasoft.com) | Dataset derivado da união do cadastro de iluminação pública e características dos Postos de Transformação (PTD) num patamar desdobrado geográfico pela e-REDES. |