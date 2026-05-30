# Relatório de Resultados Perfil Leve
**Data:** 2026-05-30 12:11

## Métricas (K-Fold CV)
| Modelo | MAE | ±MAE | RMSE | ±RMSE |
|--------|-----|------|------|-------|
| Linear | 37.5241 | 0.2943 | 57.4133 | 0.8076 |
| Tree | 36.3232 | 0.2406 | 59.5901 | 1.2444 |
| SVM | 36.7257 | 0.1978 | 59.4584 | 1.0699 |
| NeuralNet | 36.0309 | 0.2125 | 56.9183 | 0.7215 |

## Diagnóstico Curvas de Aprendizagem

### NeuralNet
| | MAE (kVA) |
|---|---|
| Treino    | 37.7534 |
| Validação | 38.3312 |
| Gap       | 0.5779 |

> . TREINO ADEQUADO: curvas convergem e gap reduzido  
> O modelo generaliza bem para dados não vistos.

### Tree
| | MAE (kVA) |
|---|---|
| Treino    | 23.1753 |
| Validação | 42.4956 |
| Gap       | 19.3203 |

> ~ LIGEIRO OVERFITTING: gap moderado, aceitável  
> Considerar mais regularização ou menos profundidade.

## Teste de Significância Estatística
**Modelos:** NeuralNet vs Tree  
**Teste:** Wilcoxon Signed-Rank (α = 0.05)  
**Justificação:** Pelo menos uma distribuição não é normal → teste não-paramétrico.
	Wilcoxon é mais robusto que Mann-Whitney para erros pareados.

| | NeuralNet | Tree |
|---|---|---|
| MAE  | 36.0309 +/- 0.2125 | 36.3232 +/- 0.2406 |
| Estatística | 5748893.0000 | / |
| p-value | 0.0000 | / |
| Resultado | **Significativo** | / |

**Melhor modelo:** NeuralNet  
A diferença é estatisticamente significativa (p=0.0000 < 0.05).