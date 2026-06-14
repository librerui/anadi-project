# Relatório de Resultados: Perfil Leve
**Data:** 2026-06-14 14:50

## Regressão: PFolga_PTD

### Métricas (K-Fold CV)
| Modelo | MAE | +/-MAE | RMSE | +/-RMSE |
|--------|-----|------|------|-------|
| Linear | 37.5241 | 0.2943 | 57.4133 | 0.8076 |
| Tree | 36.3807 | 0.2662 | 60.0568 | 1.6220 |
| SVM | 36.7257 | 0.1978 | 59.4584 | 1.0699 |
| NeuralNet | 38.0790 | 0.9333 | 59.6930 | 3.6361 |

### Diagnóstico: Curvas de Aprendizagem

#### Tree
| | MAE (kVA) |
|---|---|
| Treino    | 23.1522 |
| Validação | 42.5872 |
| Gap       | 19.4351 |

> ~ LIGEIRO OVERFITTING: gap moderado, aceitável  
> Considerar mais regularização ou menos profundidade.

#### SVM
| | MAE (kVA) |
|---|---|
| Treino    | 37.8922 |
| Validação | 38.0402 |
| Gap       | 0.1480 |

> . TREINO ADEQUADO: curvas convergem e gap reduzido  
> O modelo generaliza bem para dados não vistos.

### Teste de Significância Estatística
**Modelos:** NeuralNet vs Decision_Tree  
**Teste:** t-test Pareado (α = 0.05)  
**Justificação:** Ambas as distribuições são normais: teste paramétrico.

| | NeuralNet | Decision_Tree |
|---|---|---|
| MAE | 36.3807 +/- 0.9333 | 36.7257 +/- 0.2662 |
| Estatística | 3.5689 | / |
| p-value     | 0.0703 | / |
| Resultado   | Não significativo | / |

**Melhor modelo (regressão):** NeuralNet  
A diferença não é estatisticamente significativa (p=0.0703 ≥ 0.05).  
Ambos os modelos são equivalentes: NeuralNet tem MAE ligeiramente inferior.

---

## Classificação: utilizRede

### Métricas Globais (K-Fold CV)
| Modelo | Accuracy | +/-Acc | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|----------|------|-----------|-------|--------|------|----|-----|
| Decision_Tree | 0.5828 | 0.0159 | 0.5794 | 0.0149 | 0.5828 | 0.0159 | 0.5798 | 0.0158 |
| NeuralNet | 0.6312 | 0.0107 | 0.6287 | 0.0078 | 0.6312 | 0.0107 | 0.6120 | 0.0113 |
| SVM | 0.5916 | 0.0107 | 0.6295 | 0.0112 | 0.5916 | 0.0107 | 0.5171 | 0.0176 |
| KNN | 0.5808 | 0.0143 | 0.5701 | 0.0129 | 0.5808 | 0.0143 | 0.5641 | 0.0166 |

### Métricas por Classe

#### Decision_Tree  (Accuracy: 0.5828 +/- 0.0159)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.5687 | 0.0033 | 0.5070 | 0.0298 | 0.5357 | 0.0173 |
| baixo | 0.4570 | 0.0072 | 0.4320 | 0.0399 | 0.4432 | 0.0209 |
| medio | 0.6303 | 0.0200 | 0.6737 | 0.0188 | 0.6512 | 0.0183 |
| GLOBAL (weighted) | 0.5520 | 0.0101 | 0.5376 | 0.0295 | 0.5434 | 0.0188 |

#### NeuralNet  (Accuracy: 0.6312 +/- 0.0107)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.6834 | 0.0501 | 0.5180 | 0.0631 | 0.5841 | 0.0295 |
| baixo | 0.5406 | 0.0115 | 0.3173 | 0.1011 | 0.3904 | 0.0738 |
| medio | 0.6365 | 0.0181 | 0.8008 | 0.0603 | 0.7076 | 0.0195 |
| GLOBAL (weighted) | 0.6201 | 0.0266 | 0.5453 | 0.0748 | 0.5607 | 0.0410 |

#### SVM  (Accuracy: 0.5916 +/- 0.0107)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.7215 | 0.0271 | 0.2044 | 0.0169 | 0.3178 | 0.0178 |
| baixo | 0.6524 | 0.0281 | 0.1430 | 0.0359 | 0.2316 | 0.0456 |
| medio | 0.5788 | 0.0123 | 0.9373 | 0.0189 | 0.7155 | 0.0096 |
| GLOBAL (weighted) | 0.6509 | 0.0225 | 0.4282 | 0.0239 | 0.4216 | 0.0243 |

#### KNN  (Accuracy: 0.5808 +/- 0.0143)
| Classe | Precision | +/-Prec | Recall | +/-Rec | F1 | +/-F1 |
|--------|-----------|-------|--------|------|----|-----|
| alto | 0.5472 | 0.0263 | 0.3826 | 0.0297 | 0.4489 | 0.0150 |
| baixo | 0.4937 | 0.0152 | 0.3460 | 0.0169 | 0.4065 | 0.0124 |
| medio | 0.6091 | 0.0228 | 0.7599 | 0.0019 | 0.6760 | 0.0147 |
| GLOBAL (weighted) | 0.5500 | 0.0214 | 0.4962 | 0.0162 | 0.5105 | 0.0140 |

### Melhor e Pior Modelo por Métrica
| Métrica | Melhor | Pior |
|---------|--------|------|
| Accuracy | NeuralNet | KNN |
| Precision | SVM | KNN |
| Recall | NeuralNet | KNN |
| F1-Score | NeuralNet | SVM |

### Curvas de Aprendizagem

#### Melhor: NeuralNet
| | F1 (weighted) |
|---|---|
| Treino    | 0.6237 |
| Validação | 0.5922 |
| Gap       | -0.0315 |

> Treino adequado: curvas convergem

#### Pior: SVM
| | F1 (weighted) |
|---|---|
| Treino    | 0.5189 |
| Validação | 0.5152 |
| Gap       | -0.0038 |

> Treino adequado: curvas convergem

### Teste de Significância Estatística
**Modelos:** NeuralNet vs Decision_Tree  
**Teste:** t-test Pareado (α = 0.05)  
**Justificação:** Ambas as distribuições são normais: teste paramétrico.

| | NeuralNet | Decision_Tree |
|---|---|---|
| F1          | 0.6120 +/- 0.0113 | 0.5798 +/- 0.0158 |
| Estatística | 3.5689 | / |
| p-value     | 0.0703 | / |
| Resultado   | Não significativo | / |

**Melhor modelo (classificação):** N