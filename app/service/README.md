# Serviço API

Este módulo implementa o backend da aplicação ANADI. A sua função é servir os modelos treinados através de uma API REST, permitindo que o frontend e outros clientes executem previsões, simulações e consultas de estado sem necessidade de aceder diretamente aos notebooks ou ficheiros de treino.

## Objetivo

O serviço abstrai a lógica de negócio da aplicação e organiza-a em camadas:

- [api](api/): definição das rotas e configuração da aplicação FastAPI;
- [services](services/): orquestração das operações de predição e simulação;
- [repositories](repositories/): carregamento dos artefactos de modelos a partir da pasta [models](../models/README.md);
- [schemas](schemas/): contratos de entrada e saída validados com Pydantic;
- [core](core/): configuração, logging e utilidades transversais.

## Como iniciar

A partir da pasta [app](../README.md):

```bash
make serve
```

Ou diretamente nesta pasta:

```bash
make serve
```

A API fica disponível em:

- http://localhost:8000/api/v1
- documentação Swagger em http://localhost:8000/api/docs

## Endpoints principais

A documentação da API está presente na pasta [api](../docs/04%20-%20api/)