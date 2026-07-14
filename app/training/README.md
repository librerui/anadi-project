# Pipeline de treino

Este módulo é responsável por transformar os dados de PTD numa coleção de modelos treinados e métricas de avaliação. É a camada que conecta os dados brutos do projeto de investigação com a aplicação web, produzindo artefactos reutilizáveis pelo backend.

## O que faz

O pipeline de treino:

- carrega o dataset preparado em [PROJECT_2/data](../../PROJECT_2/data/);
- prepara as features necessárias para regressão e classificação;
- treina modelos para diferentes perfis de risco e exigência computacional;
- grava modelos, scalers, mapeamentos e resultados em [models](../models/README.md).

## Perfis disponíveis

Os treinos actualmente podem ser executados com três perfis:

- leve: treino rápido e mais leve, útil para desenvolvimento;
- regular: configuração intermédia;
- pesado: treino mais completo, indicado para validação final.

## Como executar

A partir da pasta [app](../README.md):

```bash
make train-leve
make train-regular
make train-pesado
make train-all
```

Também é possível correr diretamente a partir desta pasta:

```bash
make train-leve
```
