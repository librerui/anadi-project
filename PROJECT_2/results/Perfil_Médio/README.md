# Relatório de Resultados: Perfil Médio
**Data:** 2026-05-30 14:40

## Regressão: PFolga_PTD

### Métricas (K-Fold CV)
| Modelo | MAE | +/-MAE | RMSE | +/-RMSE |
|--------|-----|------|------|-------|
| Linear | 37.4969 | 0.2423 | 57.3225 | 0.6420 |
| Tree | 36.3664 | 0.2719 | 59.1251 | 1.0318 |
| SVM | 36.7167 | 0.2297 | 59.4238 | 0.9145 |
| NeuralNet | 35.6557 | 0.7148 | 56.7240 | 1.0049 |

### Diagnóstico: Curvas de Aprendizagem

#### NeuralNet
| | MAE (kVA) |
|---|---|
| Treino    | 36.5571 |
| Validação | 36.7576 |
| Gap       | 0.2005 |

> . TREINO ADEQUADO: curvas convergem e gap reduzido  
> O modelo generaliza bem para dados não vistos.

#### Tree
| | MAE (kVA) |
|---|---|
| Treino    | 29.1332 |
| Validação | 38.8976 |
| Gap       | 9.7643 |

> . TREINO ADEQUADO: curvas convergem e gap reduzido  
> O modelo generaliza bem para dados não vistos.

### Teste de Significância Estatística
**Modelos:** NeuralNet vs Decision_Tree  
**Teste:** t-test Pareado (α = 0.05)  
**Justificação:** Ambas as distribuições são normais: teste paramétrico.

| | NeuralNet | Decision_Tree |
|---|---|---|
| MAE | 35.6557 +/- 0.7148 | 36.3664 +/- 0.2719 |
| Estatística | 4.6659 | / |
| p-value     | 0.0095 | / |
| Resultado   | **Significativo:** | / |

**Melhor modelo (regressão):** NeuralNet  
A diferença é estatisticamente significativa (p=0.0095 < 0.05).

---

## Classificação: utilizRede

### Métricas Globais (K-Fold CV)
| Modelo | Accuracy | +/-Acc | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|----------|------|-----------|-------|--------|------|----|-----|
| Decision_Tree | 0.6449 | 0.0123 | 0.6261 | 0.0125 | 0.6449 | 0.0123 | 0.6313 | 0.0114 |
| NeuralNet | 0.6672 | 0.0088 | 0.6453 | 0.0089 | 0.6672 | 0.0088 | 0.6482 | 0.0091 |
| SVM | 0.6239 | 0.0060 | 0.5969 | 0.0169 | 0.6239 | 0.0060 | 0.5422 | 0.0079 |
| KNN | 0.6360 | 0.0065 | 0.6072 | 0.0076 | 0.6360 | 0.0065 | 0.6132 | 0.0076 |

### Métricas por Classe

#### Decision_Tree  (Accuracy: 0.6449 +/- 0.0123)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6190 | 0.0274 | 0.5455 | 0.0251 | 0.5798 | 0.0247 |
| baixo | 0.7278 | 0.0044 | 0.8431 | 0.0163 | 0.7811 | 0.0082 |
| medio | 0.4239 | 0.0245 | 0.3343 | 0.0262 | 0.3733 | 0.0220 |
| GLOBAL (weighted) | 0.5902 | 0.0188 | 0.5743 | 0.0225 | 0.5781 | 0.0183 |

#### NeuralNet  (Accuracy: 0.6672 +/- 0.0088)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6524 | 0.0150 | 0.5887 | 0.0424 | 0.6178 | 0.0224 |
| baixo | 0.7283 | 0.0142 | 0.8751 | 0.0196 | 0.7948 | 0.0086 |
| medio | 0.4674 | 0.0221 | 0.3162 | 0.0289 | 0.3762 | 0.0223 |
| GLOBAL (weighted) | 0.6161 | 0.0171 | 0.5933 | 0.0303 | 0.5963 | 0.0178 |

#### SVM  (Accuracy: 0.6239 +/- 0.0060)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6215 | 0.0166 | 0.5309 | 0.0112 | 0.5726 | 0.0128 |
| baixo | 0.6272 | 0.0045 | 0.9528 | 0.0013 | 0.7564 | 0.0033 |
| medio | 0.5101 | 0.0552 | 0.0387 | 0.0062 | 0.0720 | 0.0112 |
| GLOBAL (weighted) | 0.5863 | 0.0254 | 0.5075 | 0.0062 | 0.4670 | 0.0091 |

#### KNN  (Accuracy: 0.6360 +/- 0.0065)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.5685 | 0.0115 | 0.5679 | 0.0138 | 0.5681 | 0.0098 |
| baixo | 0.7148 | 0.0070 | 0.8537 | 0.0088 | 0.7781 | 0.0070 |
| medio | 0.4241 | 0.0124 | 0.2555 | 0.0180 | 0.3187 | 0.0171 |
| GLOBAL (weighted) | 0.5691 | 0.0103 | 0.5591 | 0.0135 | 0.5550 | 0.0113 |

### Melhor e Pior Modelo por Métrica
| Métrica | Melhor | Pior |
|---------|--------|------|
| Accuracy | NeuralNet | SVM |
| Precision | NeuralNet | SVM |
| Recall | NeuralNet | SVM |
| F1-Score | NeuralNet | SVM |

### Curvas de Aprendizagem

#### Melhor: NeuralNet
| | F1 (weighted) |
|---|---|
| Treino    | 0.6578 |
| Validação | 0.6454 |
| Gap       | -0.0124 |

> Treino adequado: curvas convergem

#### Pior: SVM
| | F1 (weighted) |
|---|---|
| Treino    | 0.5419 |
| Validação | 0.5410 |
| Gap       | -0.0009 |

> Treino adequado: curvas convergem

### Teste de Significância Estatística
**Modelos:** NeuralNet vs Decision_Tree  
**Teste:** t-test Pareado (α = 0.05)  
**Justificação:** Ambas as distribuições são normais: teste paramétrico.

| | NeuralNet | Decision_Tree |
|---|---|---|
| F1          | 0.6482 +/- 0.0091 | 0.6313 +/- 0.0114 |
| Estatística | 4.6659 | / |
| p-value     | 0.0095 | / |
| Resultado   | **Significativo:** | / |

**Melhor modelo (classificação):** N