# Relatório de Resultados: Perfil Pesado
**Data:** 2026-06-14 02:00

## Regressão: PFolga_PTD

### Métricas (K-Fold CV)
| Modelo | MAE | +/-MAE | RMSE | +/-RMSE |
|--------|-----|------|------|-------|
| Linear | 37.4980 | 0.4729 | 57.3122 | 1.2487 |
| Tree | 36.2798 | 0.3471 | 58.7240 | 1.7168 |
| SVM | 36.7155 | 0.4099 | 59.3777 | 1.3465 |
| NeuralNet | 35.4188 | 0.4511 | 55.3492 | 1.6302 |

### Diagnóstico: Curvas de Aprendizagem

#### NeuralNet
| | MAE (kVA) |
|---|---|
| Treino    | 34.8946 |
| Validação | 35.2995 |
| Gap       | 0.4049 |

> . TREINO ADEQUADO: curvas convergem e gap reduzido  
> O modelo generaliza bem para dados não vistos.

#### Tree
| | MAE (kVA) |
|---|---|
| Treino    | 32.5592 |
| Validação | 36.5107 |
| Gap       | 3.9515 |

> . TREINO ADEQUADO: curvas convergem e gap reduzido  
> O modelo generaliza bem para dados não vistos.

### Teste de Significância Estatística
**Modelos:** NeuralNet vs Decision_Tree  
**Teste:** t-test Pareado (α = 0.05)  
**Justificação:** Ambas as distribuições são normais: teste paramétrico.

| | NeuralNet | Decision_Tree |
|---|---|---|
| MAE | 35.4188 +/- 0.4511 | 36.2798 +/- 0.3471 |
| Estatística | 3.0367 | / |
| p-value     | 0.0141 | / |
| Resultado   | **Significativo:** | / |

**Melhor modelo (regressão):** NeuralNet  
A diferença é estatisticamente significativa (p=0.0141 < 0.05).

---

## Classificação: utilizRede

### Métricas Globais (K-Fold CV)
| Modelo | Accuracy | +/-Acc | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|----------|------|-----------|-------|--------|------|----|-----|
| Decision_Tree | 0.6477 | 0.0059 | 0.6464 | 0.0061 | 0.6477 | 0.0059 | 0.6418 | 0.0059 |
| NeuralNet | 0.6557 | 0.0082 | 0.6554 | 0.0080 | 0.6557 | 0.0082 | 0.6490 | 0.0092 |
| SVM | 0.5934 | 0.0072 | 0.6245 | 0.0070 | 0.5934 | 0.0072 | 0.5168 | 0.0097 |
| KNN | 0.6393 | 0.0077 | 0.6376 | 0.0081 | 0.6393 | 0.0077 | 0.6344 | 0.0075 |

### Métricas por Classe

#### Decision_Tree  (Accuracy: 0.6477 +/- 0.0059)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6843 | 0.0113 | 0.5107 | 0.0187 | 0.5846 | 0.0124 |
| baixo | 0.5392 | 0.0187 | 0.4899 | 0.0284 | 0.5129 | 0.0184 |
| medio | 0.6698 | 0.0097 | 0.7667 | 0.0114 | 0.7149 | 0.0064 |
| GLOBAL (weighted) | 0.6311 | 0.0133 | 0.5891 | 0.0195 | 0.6041 | 0.0124 |

#### NeuralNet  (Accuracy: 0.6557 +/- 0.0082)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.7085 | 0.0192 | 0.5311 | 0.0344 | 0.6062 | 0.0206 |
| baixo | 0.5441 | 0.0257 | 0.4730 | 0.0472 | 0.5037 | 0.0218 |
| medio | 0.6737 | 0.0120 | 0.7788 | 0.0228 | 0.7221 | 0.0085 |
| GLOBAL (weighted) | 0.6421 | 0.0190 | 0.5943 | 0.0348 | 0.6107 | 0.0170 |

#### SVM  (Accuracy: 0.5934 +/- 0.0072)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.7387 | 0.0191 | 0.1880 | 0.0098 | 0.2995 | 0.0125 |
| baixo | 0.6019 | 0.0281 | 0.1412 | 0.0110 | 0.2285 | 0.0154 |
| medio | 0.5830 | 0.0084 | 0.9397 | 0.0037 | 0.7195 | 0.0060 |
| GLOBAL (weighted) | 0.6412 | 0.0185 | 0.4229 | 0.0082 | 0.4158 | 0.0113 |

#### KNN  (Accuracy: 0.6393 +/- 0.0077)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6711 | 0.0179 | 0.5177 | 0.0140 | 0.5842 | 0.0093 |
| baixo | 0.5181 | 0.0168 | 0.4811 | 0.0161 | 0.4987 | 0.0135 |
| medio | 0.6674 | 0.0091 | 0.7518 | 0.0143 | 0.7070 | 0.0083 |
| GLOBAL (weighted) | 0.6189 | 0.0146 | 0.5835 | 0.0148 | 0.5966 | 0.0104 |

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
| Treino    | 0.6573 |
| Validação | 0.6469 |
| Gap       | -0.0104 |

> Treino adequado: curvas convergem

#### Pior: SVM
| | F1 (weighted) |
|---|---|
| Treino    | 0.5167 |
| Validação | 0.5164 |
| Gap       | -0.0002 |

> Treino adequado: curvas convergem

### Teste de Significância Estatística
**Modelos:** NeuralNet vs Decision_Tree  
**Teste:** t-test Pareado (α = 0.05)  
**Justificação:** Ambas as distribuições são normais: teste paramétrico.

| | NeuralNet | Decision_Tree |
|---|---|---|
| F1          | 0.6490 +/- 0.0092 | 0.6418 +/- 0.0059 |
| Estatística | 3.0367 | / |
| p-value     | 0.0141 | / |
| Resultado   | **Significativo:** | / |

**Melhor modelo (classificação):** N