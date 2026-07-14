# Projeto ANADI: Viabilidade da Integração de VE na Rede de Distribuição Portuguesa

> Repositório central do projeto desenvolvido no âmbito da unidade curricular de **Análise de Dados em Informática** (ANADI) do curso de Engenharia Informática do ISEP (ano letivo 2025/2026).

Este projeto tem como objetivo avaliar, analisar e prever a capacidade da rede elétrica portuguesa (baseada em dados abertos da e-REDES) para suportar a instalação de carregadores de Veículos Elétricos (VE), com foco na capacidade libertada através da modernização da Iluminação Pública para a tecnologia LED.

## Módulos do Projeto

### [Análise Estatística](./PROJECT_1/README.md)
Avaliação estatística agregada (por concelho) da rede, testes de hipóteses, análise exploratória e regressão OLS.

### [Aprendizagem Automática](./PROJECT_2/README.md)
Modelação preditiva granular (ao nível do PTD) usando algoritmos de Regressão e Classificação para avaliar a estabilidade e cenários de carga.

## [Aplicação](./app/README.md)

A aplicação consolidada desta pesquisa e uma interface web para interagir com os modelos treinados estão na pasta [app](./app/README.md).

Para um mapa da documentação e navegação rápida entre os ficheiros de
documentação veja: [app/docs](./app/docs/README.md).

## Estrutura do Repositório

O repositório está organizado para separar os dados, os notebooks de análise e a componente científica de cada fase. Abaixo encontra-se a arquitetura principal:

* **`PROJECT_1/`** (Análise Estatística).
    * `data/`: Datasets originais (`IP_data.xlsx`, `PTD_data.xlsx`, `densidade.csv`).
    * `article/`: Artigo científico em LaTeX e PDF, e respetivas imagens.
    * `main.ipynb`: Notebook de exploração de dados e estatística.
    * `dashboard.py`: Aplicação Streamlit de visualização de dados agregados.
* **`PROJECT_2/`** (Aprendizagem Automática).
    * `data/`: Dataset processado ao nível do PTD (`PTD_level_dataset.xlsx`).
    * `profiles/`: Configurações em JSON dos perfis de simulação (Leve, Regular, Pesado).
    * `results/`: Persistência de modelos treinados (`.pkl`), métricas e mapeamentos geográficos separados por perfil, reports em markdown dos resultados de execução.
    * `article/`: Artigo científico em LaTeX e PDF, e respetivas imagens.
    * `main.ipynb` e `compare.ipynb`: Notebooks de treino, teste e comparação dos modelos.
    * `prediction.py`: Aplicação interativa para inferência do modelo com base no input do utilizador.
* **`app/`** (Solução).
    * `training/`: Pipeline de treino, preparação de features e geração de artefactos modelados.
    * `service/`: Backend FastAPI que expõe os modelos para previsões e simulações.
    * `models/`: Armazenamento dos modelos treinados e respetivos metadados.
    * `frontend/`: Interface web em Vue para consulta e análise interativa.
    * `docs/`: Documentação do projeto, incluindo teoria, API, frontend e backend.

## Autores
- Rui Santiago ([Rui-San](https://github.com/Rui-San)), Departamento de Engenharia Informática do ISEP, 3.º ano, 2.º semestre, 2025/2026
- Rui Silva ([librerui](https://github.com/librerui)), Departamento de Engenharia Informática do ISEP, 3.º ano, 2.º semestre, 2025/2026
- Tiago Barros ([Sagiri721](https://github.com/Sagiri721)), Departamento de Engenharia Informática do ISEP, 3.º ano, 2.º semestre, 2025/2026