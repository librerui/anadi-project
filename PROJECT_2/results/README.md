Os resultados parecem espetáveis e consistentes. Algumas observações:

Consistência entre perfis — os valores entre Leve e Médio são muito próximos (diferença < 0.5 kVA), o que é um bom sinal. Significa que o subsampling não está a distorcer os resultados e o perfil Leve é fiável para desenvolvimento.

Ranking dos modelos — NeuralNet ganha em MAE, Linear ganha em RMSE no perfil Médio. Isso é interessante para o artigo — significa que a rede neuronal erra menos em média mas o modelo linear lida melhor com os outliers (RMSE penaliza erros grandes).

Os erros em si — MAE ~36 kVA e RMSE ~57 kVA num target que pelos dados anteriores tem média ~148 kVA e std ~187 kVA. Não é um erro desprezável, mas é razoável dado que estás a prever com uma única variável de regressão simples... espera, o MAE da regressão múltipla também é 37? Isso seria estranho.