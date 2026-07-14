# Modelos persistidos

Esta pasta guarda os artefactos gerados pelo pipeline de treino e utilizados pelo backend da aplicação.

## Organização

Cada execução de treino cria uma versão isolada de modelos, organizada por perfil e timestamp. Isso permite comparar diferentes versões de forma simples e manter o serviço alinhado com a configuração que foi validada.

## Conteúdo típico

Uma versão de resultados pode incluir:

- modelos de regressão e classificação;
- scalers treinados para normalização;
- mapeamentos geográficos e de codificação;
- ficheiros JSON com métricas, curvas de aprendizagem e configuração do treino.