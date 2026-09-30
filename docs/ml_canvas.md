# ML Canvas — previsão de churn

Sistema entregue ao fim da Fase 1 do Tech Challenge. Versão visual: [ml_canvas.html](ml_canvas.html).

## Canvas

| Bloco | Definição |
|---|---|
| Proposta de valor | Apontar, para a diretoria e o time de retenção, os clientes com maior risco de cancelar, para agir antes que saiam. |
| Tarefa de ML | Classificação binária. Entrada: dados do cliente. Saída: propensão de churn, entre 0 e 1. |
| Decisões | Propensão acima do limiar: cliente em risco, entra na ação de retenção. O limiar é o de menor custo de negócio, não 0,5. |
| Fazer predições | API FastAPI com o modelo campeão. `GET /health` informa se está no ar. `POST /predict` recebe um cliente e devolve propensão e risco. |
| Fontes de dados | Telco Customer Churn (IBM), em `data/raw/`: 7.043 clientes, 21 colunas, 26,5% de churn. |
| Coleta de dados | Base estática. Um novo treino exige uma nova extração com o mesmo formato. |
| Features | 17 variáveis de contrato, serviços, tempo de casa e cobrança, tratadas num `Pipeline` do Scikit-Learn. |
| Construção de modelos | Regressão Logística (baseline), Random Forest e `MLPClassifier`, com validação cruzada e seed fixa. O campeão é salvo em `.joblib`. |
| Avaliação offline | AUC-ROC e F1 comparam os modelos. O custo de negócio escolhe o campeão e o limiar. |
| Monitoramento | `/health` no ar, testes com pytest, Model Card com desempenho, limitações e vieses. |

## Stakeholders

| Quem | Papel |
|---|---|
| Diretoria | Pediu o modelo. Acompanha o churn e o custo de retenção. |
| Time de retenção | Usa a propensão para priorizar quem contatar. |
| Time de dados (o grupo) | Treina, compara, serve a API e documenta. |
| Cliente | É afetado pela ação. Gênero não entra no modelo. |

## Métricas

**Negócio.** Custo = `FN × C_fn + FP × C_fp`.

- `FN`: cliente que cancela sem ser abordado. `C_fn` é a receita perdida: `cobranca_mensal` × meses de receita.
- `FP`: ação de retenção em quem não ia cancelar. `C_fp` é o custo de um contato.

`C_fn` e `C_fp` são premissas do grupo, registradas no Model Card.

**Técnicas.** AUC-ROC mede a ordenação dos clientes sem depender do limiar. F1 equilibra precisão e recall na classe churn. Acurácia não entra: com 26,5% de churn, dizer “ninguém cancela” já acerta 73,5%.

**Campeão.** O modelo de menor custo na validação cruzada. Se a diferença couber na variação entre os folds, fica o mais simples.

## Dados e features

- `Churn` vira `target`: `Yes = 1`, `No = 0`.
- Saem `id_cliente` (identificador), `genero` e `dependentes` (sensíveis).
- Saem os 11 clientes com 0 meses de casa e cobrança vazia. Restam 7.032, com 26,6% de churn.
- Sim/Não viram 1/0. “Sem internet” e “sem telefone” também viram 0.
- Tipo de internet e forma de pagamento vão em one-hot, porque não têm ordem. Tipo de contrato mantém a ordem: mensal, 1 ano, 2 anos.
- Cobrança mensal e total cobrado são numéricos. O total cobrado é acumulado no tempo de casa.

## Contrato da API

| Endpoint | Entrada | Saída |
|---|---|---|
| `GET /health` | — | Status da API e versão do modelo. |
| `POST /predict` | As 17 variáveis de um cliente. | Propensão de churn (0 a 1) e se o cliente está em risco. |
