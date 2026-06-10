# Relatório de Resultados: Perfil Pesado
**Data:** 2026-06-10 17:19

## Regressão: PFolga_PTD

### Métricas (K-Fold CV)
| Modelo | MAE | +/-MAE | RMSE | +/-RMSE |
|--------|-----|------|------|-------|
| Linear | 37.4980 | 0.4729 | 57.3122 | 1.2487 |
| Tree | 36.3154 | 0.3527 | 58.8461 | 1.5633 |
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
| MAE | 35.4188 +/- 0.4511 | 36.3154 +/- 0.3527 |
| Estatística | 11.7859 | / |
| p-value     | 0.0000 | / |
| Resultado   | **Significativo:** | / |

**Melhor modelo (regressão):** NeuralNet  
A diferença é estatisticamente significativa (p=0.0000 < 0.05).

---

## Classificação: utilizRede

### Métricas Globais (K-Fold CV)
| Modelo | Accuracy | +/-Acc | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|----------|------|-----------|-------|--------|------|----|-----|
| Decision_Tree | 0.6605 | 0.0055 | 0.6400 | 0.0052 | 0.6605 | 0.0055 | 0.6443 | 0.0047 |
| NeuralNet | 0.6785 | 0.0051 | 0.6609 | 0.0041 | 0.6785 | 0.0051 | 0.6623 | 0.0044 |
| SVM | 0.6220 | 0.0074 | 0.5959 | 0.0099 | 0.6220 | 0.0074 | 0.5398 | 0.0103 |
| KNN | 0.6605 | 0.0042 | 0.6359 | 0.0041 | 0.6605 | 0.0042 | 0.6401 | 0.0046 |

### Métricas por Classe

#### Decision_Tree  (Accuracy: 0.6605 +/- 0.0055)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6390 | 0.0180 | 0.5705 | 0.0167 | 0.6025 | 0.0097 |
| baixo | 0.7291 | 0.0050 | 0.8626 | 0.0086 | 0.7903 | 0.0047 |
| medio | 0.4573 | 0.0156 | 0.3325 | 0.0180 | 0.3847 | 0.0137 |
| GLOBAL (weighted) | 0.6085 | 0.0128 | 0.5885 | 0.0144 | 0.5925 | 0.0094 |

#### NeuralNet  (Accuracy: 0.6785 +/- 0.0051)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6809 | 0.0165 | 0.5835 | 0.0276 | 0.6278 | 0.0126 |
| baixo | 0.7332 | 0.0070 | 0.8799 | 0.0117 | 0.7998 | 0.0050 |
| medio | 0.4922 | 0.0219 | 0.3570 | 0.0230 | 0.4130 | 0.0145 |
| GLOBAL (weighted) | 0.6355 | 0.0152 | 0.6068 | 0.0207 | 0.6135 | 0.0107 |

#### SVM  (Accuracy: 0.6220 +/- 0.0074)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6308 | 0.0168 | 0.5197 | 0.0105 | 0.5698 | 0.0105 |
| baixo | 0.6226 | 0.0083 | 0.9543 | 0.0038 | 0.7535 | 0.0064 |
| medio | 0.5064 | 0.0323 | 0.0388 | 0.0071 | 0.0719 | 0.0122 |
| GLOBAL (weighted) | 0.5866 | 0.0191 | 0.5043 | 0.0072 | 0.4651 | 0.0097 |

#### KNN  (Accuracy: 0.6605 +/- 0.0042)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6216 | 0.0154 | 0.5964 | 0.0171 | 0.6084 | 0.0093 |
| baixo | 0.7267 | 0.0075 | 0.8690 | 0.0055 | 0.7915 | 0.0054 |
| medio | 0.4626 | 0.0138 | 0.2947 | 0.0089 | 0.3598 | 0.0061 |
| GLOBAL (weighted) | 0.6036 | 0.0122 | 0.5867 | 0.0105 | 0.5866 | 0.0070 |

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
| Treino    | 0.6705 |
| Validação | 0.6611 |
| Gap       | -0.0093 |

> Treino adequado: curvas convergem

#### Pior: SVM
| | F1 (weighted) |
|---|---|
| Treino    | 0.5400 |
| Validação | 0.5398 |
| Gap       | -0.0002 |

> Treino adequado: curvas convergem

### Teste de Significância Estatística
**Modelos:** NeuralNet vs Decision_Tree  
**Teste:** t-test Pareado (α = 0.05)  
**Justificação:** Ambas as distribuições são normais: teste paramétrico.

| | NeuralNet | Decision_Tree |
|---|---|---|
| F1          | 0.6623 +/- 0.0044 | 0.6443 +/- 0.0047 |
| Estatística | 11.7859 | / |
| p-value     | 0.0000 | / |
| Resultado   | **Significativo:** | / |

**Melhor modelo (classificação):** N