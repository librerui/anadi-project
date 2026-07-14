# Aplicação

Esta pasta reúne a versão operacional do projeto ANADI: uma aplicação web que transforma as conclusões das fases de investigação em uma solução utilizável para análise de viabilidade de carregadores de Veículos Elétricos (VE) na rede de distribuição portuguesa.

Enquanto os projetos de investigação em [PROJECT_1](../PROJECT_1/README.md) e [PROJECT_2](../PROJECT_2/README.md) exploram os dados e validam modelos, a pasta [app](.) consolida esse trabalho num produto que permite:

- treinar e versionar modelos preditivos;
- disponibilizar previsões e simulações através de uma API REST;
- oferecer uma interface web para interação com utilizadores;
- apoiar decisões de planeamento da rede sem depender de notebooks.

## Componentes principais

- [training](training/README.md): pipeline de treino, preparação de features e geração de artefactos modelados.
- [service](service/README.md): backend FastAPI que expõe os modelos para previsões e simulações.
- [models](models/README.md): armazenamento dos modelos treinados e respetivos metadados.
- [frontend](frontend/README.md): interface web em Vue para consulta e análise interativa.

## Fluxo típico

1. O pipeline de treino gera modelos a partir do dataset de PTD.
2. Os modelos são guardados em versões organizadas por perfil.
3. O serviço carrega esses artefactos e expõe endpoints de predição.
4. O frontend consome a API e apresenta os resultados em páginas de previsão, simulação e análise regional.

## Como executar

A partir da raiz da pasta [app](.):

```bash
make help
make train-leve
make serve
make frontend-dev
```

Este conjunto de comandos permite preparar os modelos, iniciar o backend e abrir o frontend em modo de desenvolvimento.