# Relatório de Resultados: Perfil Leve
**Data:** 2026-06-10 14:47

## Regressão: PFolga_PTD

### Métricas (K-Fold CV)
| Modelo | MAE | +/-MAE | RMSE | +/-RMSE |
|--------|-----|------|------|-------|
| Linear | 37.5241 | 0.2943 | 57.4133 | 0.8076 |
| Tree | 36.3655 | 0.2244 | 59.8527 | 1.4680 |
| SVM | 36.7257 | 0.1978 | 59.4584 | 1.0699 |
| NeuralNet | 36.0309 | 0.2125 | 56.9183 | 0.7215 |

### Diagnóstico: Curvas de Aprendizagem

#### NeuralNet
| | MAE (kVA) |
|---|---|
| Treino    | 37.7534 |
| Validação | 38.3312 |
| Gap       | 0.5779 |

> . TREINO ADEQUADO: curvas convergem e gap reduzido  
> O modelo generaliza bem para dados não vistos.

#### Tree
| | MAE (kVA) |
|---|---|
| Treino    | 23.1522 |
| Validação | 42.5872 |
| Gap       | 19.4351 |

> ~ LIGEIRO OVERFITTING: gap moderado, aceitável  
> Considerar mais regularização ou menos profundidade.

### Teste de Significância Estatística
**Modelos:** NeuralNet vs Decision_Tree  
**Teste:** t-test Pareado (α = 0.05)  
**Justificação:** Ambas as distribuições são normais: teste paramétrico.

| | NeuralNet | Decision_Tree |
|---|---|---|
| MAE | 36.0309 +/- 0.2125 | 36.3655 +/- 0.2244 |
| Estatística | 3.2679 | / |
| p-value     | 0.0823 | / |
| Resultado   | Não significativo | / |

**Melhor modelo (regressão):** NeuralNet  
A diferença não é estatisticamente significativa (p=0.0823 ≥ 0.05).  
Ambos os modelos são equivalentes: NeuralNet tem MAE ligeiramente inferior.

---

## Classificação: utilizRede

### Métricas Globais (K-Fold CV)
| Modelo | Accuracy | +/-Acc | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|----------|------|-----------|-------|--------|------|----|-----|
| Decision_Tree | 0.6136 | 0.0119 | 0.5987 | 0.0138 | 0.6136 | 0.0119 | 0.6038 | 0.0130 |
| NeuralNet | 0.6534 | 0.0067 | 0.6229 | 0.0143 | 0.6534 | 0.0067 | 0.6169 | 0.0170 |
| SVM | 0.6158 | 0.0041 | 0.5727 | 0.0192 | 0.6158 | 0.0041 | 0.5305 | 0.0064 |
| KNN | 0.5916 | 0.0066 | 0.5611 | 0.0081 | 0.5916 | 0.0066 | 0.5679 | 0.0097 |

### Métricas por Classe

#### Decision_Tree  (Accuracy: 0.6136 +/- 0.0119)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.5835 | 0.0161 | 0.5471 | 0.0301 | 0.5645 | 0.0215 |
| baixo | 0.7108 | 0.0107 | 0.7909 | 0.0165 | 0.7486 | 0.0074 |
| medio | 0.3863 | 0.0318 | 0.3220 | 0.0335 | 0.3502 | 0.0280 |
| GLOBAL (weighted) | 0.5602 | 0.0195 | 0.5533 | 0.0267 | 0.5544 | 0.0190 |

#### NeuralNet  (Accuracy: 0.6534 +/- 0.0067)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6273 | 0.0508 | 0.5971 | 0.0460 | 0.6081 | 0.0108 |
| baixo | 0.6965 | 0.0253 | 0.9008 | 0.0284 | 0.7847 | 0.0065 |
| medio | 0.4670 | 0.0441 | 0.2079 | 0.0725 | 0.2836 | 0.0748 |
| GLOBAL (weighted) | 0.5969 | 0.0401 | 0.5686 | 0.0490 | 0.5588 | 0.0307 |

#### SVM  (Accuracy: 0.6158 +/- 0.0041)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6227 | 0.0446 | 0.5270 | 0.0148 | 0.5703 | 0.0249 |
| baixo | 0.6188 | 0.0157 | 0.9522 | 0.0142 | 0.7498 | 0.0084 |
| medio | 0.4260 | 0.0748 | 0.0250 | 0.0020 | 0.0470 | 0.0030 |
| GLOBAL (weighted) | 0.5558 | 0.0450 | 0.5014 | 0.0103 | 0.4557 | 0.0121 |

#### KNN  (Accuracy: 0.5916 +/- 0.0066)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.5108 | 0.0184 | 0.5336 | 0.0275 | 0.5209 | 0.0033 |
| baixo | 0.6815 | 0.0112 | 0.8085 | 0.0105 | 0.7394 | 0.0051 |
| medio | 0.3672 | 0.0133 | 0.2119 | 0.0195 | 0.2680 | 0.0160 |
| GLOBAL (weighted) | 0.5198 | 0.0143 | 0.5180 | 0.0192 | 0.5095 | 0.0081 |

### Melhor e Pior Modelo por Métrica
| Métrica | Melhor | Pior |
|---------|--------|------|
| Accuracy | NeuralNet | KNN |
| Precision | NeuralNet | KNN |
| Recall | NeuralNet | KNN |
| F1-Score | NeuralNet | SVM |

### Curvas de Aprendizagem

#### Melhor: NeuralNet
| | F1 (weighted) |
|---|---|
| Treino    | 0.6718 |
| Validação | 0.6339 |
| Gap       | -0.0379 |

> Treino adequado: curvas convergem

#### Pior: SVM
| | F1 (weighted) |
|---|---|
| Treino    | 0.5333 |
| Validação | 0.5287 |
| Gap       | -0.0046 |

> Treino adequado: curvas convergem

### Teste de Significância Estatística
**Modelos:** NeuralNet vs Decision_Tree  
**Teste:** t-test Pareado (α = 0.05)  
**Justificação:** Ambas as distribuições são normais: teste paramétrico.

| | NeuralNet | Decision_Tree |
|---|---|---|
| F1          | 0.6169 +/- 0.0170 | 0.6038 +/- 0.0130 |
| Estatística | 3.2679 | / |
| p-value     | 0.0823 | / |
| Resultado   | Não significativo | / |

**Melhor modelo (classificação):** N