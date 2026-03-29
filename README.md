# Viabilidade da Integração de Mobilidade Elétrica na Rede de Distribuição Portuguesa

> Análise estatística da viabilidade de integração de carregadores de veículos elétricos
> na rede de distribuição portuguesa, com base em dados reais da e-REDES.

## Contexto

Este projeto foi desenvolvido no âmbito da unidade curricular de **Análise de Dados em Informática** (ANADI) do curso de Engenharia Informática do ISEP (ano letivo 2025/2026).

O estudo avalia de que forma a substituição de iluminação pública ineficiente (sódio e mercúrio) por tecnologia LED pode libertar capacidade nos Postos de Transformação de Distribuição (PTD), e se essa capacidade é suficiente para suportar a instalação de carregadores de veículos elétricos de 22 kW sem comprometer a estabilidade da rede.

## Metodologia

A análise segue o pipeline:

1. **Manipulação de dados**: processamento de IP_data e PTD_data, criação de variáveis derivadas (Ganho LED, Folga Rede, Saldo de Viabilidade)
2. **Análise Exploratória**: mix tecnológico, boxplots por distrito, outliers, estatística descritiva
3. **Inferência Estatística**: teste t (ocupação < 60%), teste t de duas amostras (modernizados vs ineficientes), ANOVA regional com post-hoc de Tukey, correlação de Pearson
4. **Regressão**: modelo OLS com diagnóstico de multicolinearidade (VIF), verificação de resíduos (Shapiro-Wilk, Durbin-Watson, Breusch-Pagan), identificação de concelhos prioritários para VE

## Instalação e Execução

### Requisitos
- Python
- make

### Setup
```bash
git clone https://github.com/librerui/anadi-project
cd anadi-project

# Criar ambiente virtual e instalar dependências
make venv

# Ativar o ambiente
source .venv/bin/activate
```

### Executar o Dashboard
```bash
make dashboard
```

O dashboard abre em `http://localhost:8501` e inclui as páginas:

| Página | Conteúdo |
|---|---|
| Visão Geral | Métricas globais da rede |
| Perfis Horários | Consumo IP antes vs depois de LED (simulado) |
| Mix Tecnológico | LED vs convencional, curva de Pareto |
| Capacidade PTD | Boxplots por distrito, PTDs em sobrecarga |
| Potência Libertada | Ganho relativo LED por concelho e distrito |
| Cenários VE | Simulador interativo de viabilidade por carregador |
| Inferência Estatística | Robustez dos testes ao longo de 100 seeds |
| Modelo Preditivo | Regressão OLS, VIF, simulador preditivo |
| Mapa Interativo | Mapa de Portugal com capacidade VE por PTD |

### Executar o Notebook
```bash
source .venv/bin/activate

jupyter notebook main.ipynb
```

## Fontes de Dados

| Dataset | Fonte | Descrição |
|---|---|---|
| `IP_data.xlsx` | [e-REDES Open Data](https://e-redes.opendatasoft.com) | Cadastro de iluminação pública |
| `PTD_data.xlsx` | [e-REDES Open Data](https://e-redes.opendatasoft.com) | Postos de transformação de distribuição |
| `densidade.csv` | [INE](https://www.ine.pt) | Densidade populacional, Censos 2021 |

## Autores
- Rui Santiago, Departamento de Engenharia Informática do ISEP, 3.º ano, 2.º semestre, 2025/2026
- Rui Silva, Departamento de Engenharia Informática do ISEP, 3.º ano, 2.º semestre, 2025/2026
- Tiago Barros, Departamento de Engenharia Informática do ISEP, 3.º ano, 2.º semestre, 2025/2026
