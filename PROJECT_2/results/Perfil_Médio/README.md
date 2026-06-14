# Relatório de Resultados: Perfil Médio
**Data:** 2026-06-13 21:22

## Regressão: PFolga_PTD

### Métricas (K-Fold CV)
| Modelo | MAE | +/-MAE | RMSE | +/-RMSE |
|--------|-----|------|------|-------|
| Linear | 37.4969 | 0.2423 | 57.3225 | 0.6420 |
| Tree | 36.3208 | 0.2962 | 58.9004 | 1.0342 |
| SVM | 36.7167 | 0.2297 | 59.4238 | 0.9145 |
| NeuralNet | 36.7075 | 0.1465 | 57.3782 | 1.8506 |

### Diagnóstico: Curvas de Aprendizagem

#### Tree
| | MAE (kVA) |
|---|---|
| Treino    | 29.1244 |
| Validação | 38.8792 |
| Gap       | 9.7548 |

> . TREINO ADEQUADO: curvas convergem e gap reduzido  
> O modelo generaliza bem para dados não vistos.

#### NeuralNet
| | MAE (kVA) |
|---|---|
| Treino    | 36.5571 |
| Validação | 36.7576 |
| Gap       | 0.2005 |

> . TREINO ADEQUADO: curvas convergem e gap reduzido  
> O modelo generaliza bem para dados não vistos.

### Teste de Significância Estatística
**Modelos:** NeuralNet vs Decision_Tree  
**Teste:** t-test Pareado (α = 0.05)  
**Justificação:** Ambas as distribuições são normais: teste paramétrico.

| | NeuralNet | Decision_Tree |
|---|---|---|
| MAE | 36.3208 +/- 0.1465 | 36.7075 +/- 0.2962 |
| Estatística | 4.0645 | / |
| p-value     | 0.0153 | / |
| Resultado   | **Significativo:** | / |

**Melhor modelo (regressão):** NeuralNet  
A diferença é estatisticamente significativa (p=0.0153 < 0.05).

---

## Classificação: utilizRede

### Métricas Globais (K-Fold CV)
| Modelo | Accuracy | +/-Acc | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|----------|------|-----------|-------|--------|------|----|-----|
| Decision_Tree | 0.6235 | 0.0041 | 0.6229 | 0.0051 | 0.6235 | 0.0041 | 0.6204 | 0.0056 |
| NeuralNet | 0.6467 | 0.0066 | 0.6502 | 0.0079 | 0.6467 | 0.0066 | 0.6418 | 0.0108 |
| SVM | 0.5875 | 0.0078 | 0.6212 | 0.0096 | 0.5875 | 0.0078 | 0.5157 | 0.0100 |
| KNN | 0.6113 | 0.0080 | 0.6076 | 0.0088 | 0.6113 | 0.0080 | 0.6043 | 0.0087 |

### Métricas por Classe

#### Decision_Tree  (Accuracy: 0.6235 +/- 0.0041)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6408 | 0.0137 | 0.5193 | 0.0376 | 0.5730 | 0.0248 |
| baixo | 0.5173 | 0.0196 | 0.5083 | 0.0299 | 0.5116 | 0.0077 |
| medio | 0.6568 | 0.0095 | 0.7156 | 0.0238 | 0.6846 | 0.0063 |
| GLOBAL (weighted) | 0.6050 | 0.0143 | 0.5811 | 0.0304 | 0.5897 | 0.0129 |

#### NeuralNet  (Accuracy: 0.6467 +/- 0.0066)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6995 | 0.0321 | 0.5106 | 0.0298 | 0.5893 | 0.0206 |
| baixo | 0.5437 | 0.0073 | 0.5432 | 0.0936 | 0.5385 | 0.0516 |
| medio | 0.6702 | 0.0206 | 0.7487 | 0.0402 | 0.7061 | 0.0080 |
| GLOBAL (weighted) | 0.6378 | 0.0200 | 0.6008 | 0.0545 | 0.6113 | 0.0267 |

#### SVM  (Accuracy: 0.5875 +/- 0.0078)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.7363 | 0.0426 | 0.2007 | 0.0146 | 0.3153 | 0.0211 |
| baixo | 0.6081 | 0.0309 | 0.1571 | 0.0125 | 0.2496 | 0.0180 |
| medio | 0.5749 | 0.0069 | 0.9316 | 0.0055 | 0.7110 | 0.0062 |
| GLOBAL (weighted) | 0.6398 | 0.0268 | 0.4298 | 0.0108 | 0.4253 | 0.0151 |

#### KNN  (Accuracy: 0.6113 +/- 0.0080)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6225 | 0.0152 | 0.4665 | 0.0122 | 0.5333 | 0.0117 |
| baixo | 0.5166 | 0.0124 | 0.4593 | 0.0233 | 0.4860 | 0.0159 |
| medio | 0.6370 | 0.0085 | 0.7366 | 0.0066 | 0.6831 | 0.0055 |
| GLOBAL (weighted) | 0.5920 | 0.0121 | 0.5541 | 0.0141 | 0.5675 | 0.0110 |

### Melhor e Pior Modelo por Métrica
| Métrica | Melhor | Pior |
|---------|--------|------|
| Accuracy | NeuralNet | SVM |
| Precision | NeuralNet | KNN |
| Recall | NeuralNet | SVM |
| F1-Score | NeuralNet | SVM |

### Curvas de Aprendizagem

#### Melhor: NeuralNet
| | F1 (weighted) |
|---|---|
| Treino    | 0.6659 |
| Validação | 0.6448 |
| Gap       | -0.0211 |

> Treino adequado: curvas convergem

#### Pior: SVM
| | F1 (weighted) |
|---|---|
| Treino    | 0.5146 |
| Validação | 0.5135 |
| Gap       | -0.0011 |

> Treino adequado: curvas convergem

### Teste de Significância Estatística
**Modelos:** NeuralNet vs Decision_Tree  
**Teste:** t-test Pareado (α = 0.05)  
**Justificação:** Ambas as distribuições são normais: teste paramétrico.

| | NeuralNet | Decision_Tree |
|---|---|---|
| F1          | 0.6418 +/- 0.0108 | 0.6204 +/- 0.0056 |
| Estatística | 4.0645 | / |
| p-value     | 0.0153 | / |
| Resultado   | **Significativo:** | / |

**Melhor modelo (classificação):** N