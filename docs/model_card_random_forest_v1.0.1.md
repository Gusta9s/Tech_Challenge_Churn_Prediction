# Model Card — Random Forest Churn Classifier (v1.0.1)

> Formato inspirado no padrão de *Model Cards for Model Reporting*
> (Mitchell et al., 2019) e nas convenções adotadas por projetos como
> Hugging Face Model Hub e Google Model Cards. Preenchido com dados reais
> de validação cruzada (K-Fold) deste projeto — nenhum valor abaixo é
> estimado ou fictício.

## Detalhes do modelo

| Campo | Valor |
|---|---|
| Nome | `random_forest.joblib` |
| Versão | `v1.0.1` (`models/v1.0.1/random_forest.joblib`) |
| Tipo | `sklearn.ensemble.RandomForestClassifier` |
| Tarefa | Classificação binária (churn / não-churn) |
| Hiperparâmetros principais | `max_depth=12`, `min_samples_leaf=15` |
| Data de desenvolvimento | Projeto Tech Challenge — Fase 1 (FIAP) |
| Desenvolvedor | Gusta9s |
| Licença/uso | Uso acadêmico (Tech Challenge FIAP) |
| Contato | gustavoapacheco@yahoo.com.br |
| Documentos relacionados | [ML Canvas](ml_canvas.md), [Por que o Random Forest](Por%20que%20o%20Random%20Forest%20para%20ser%20o%20modelo%20campeao) |

## Uso pretendido

- **Uso primário**: estimar a probabilidade de um cliente de telecomunicações
  cancelar o serviço (*churn*), a partir de atributos contratuais,
  demográficos e de consumo já disponíveis no momento da predição, para
  **priorizar ações de retenção** (ex.: ofertas, contato proativo).
- **Usuários pretendidos**: sistemas internos de CRM/retenção e equipes de
  negócio que consomem a API REST (`POST /predict`) deste repositório.
- **Fora de escopo**: o modelo **não** deve ser usado para decisões que
  afetem direitos do cliente (ex.: negar ou alterar condições contratuais,
  score de crédito, elegibilidade a serviços) nem como única fonte de
  decisão automatizada sem revisão humana — ele serve como **sinal de
  priorização**, não como veredito.

## Dados de treinamento e avaliação

- **Dataset**: [IBM Telco Customer Churn](data/raw/Telco-Customer-Churn.csv)
  — 7.043 clientes, 20 atributos de entrada (perfil demográfico, tipo de
  contrato, serviços contratados, forma de pagamento, tempo de permanência
  e cobrança) + 1 variável alvo (`Churn`).
- **Desbalanceamento de classes**: a classe minoritária (churn) representa
  historicamente ~26% da base — desbalanceamento moderado, tratado durante
  a modelagem (comparação de modelos com e sem balanceamento de classes,
  ver histórico de experimentos em `notebooks/arvore_de_descisao/historico/`).
- **Avaliação**: **validação cruzada K-Fold estratificada**, não um único
  holdout — os números abaixo são a média e o desvio-padrão sobre todos os
  folds, o que caracteriza avaliação sobre uma carga de teste
  significativamente maior e mais representativa do que um split único.
- **Rastreabilidade**: métricas versionadas via DVC
  (`notebooks/arvore_de_descisao/modelo_final/metrics/metrics.json`,
  listado em `dvc.yaml`).

## Métricas de performance (K-Fold, média ± desvio-padrão)

| Métrica | Média | Desvio-padrão |
|---|---|---|
| ROC AUC | 0,8468 | ± 0,0109 |
| Recall (sensibilidade ao churn) | 0,7717 | ± 0,0378 |
| F1-score | 0,6348 | ± 0,0218 |
| Acurácia | 0,7657 | ± 0,0123 |
| Precisão | 0,5394 | ± 0,0159 |

**Leitura crítica dos números:**

- O **recall de 77%** é o ponto forte do modelo para o caso de uso de
  retenção: ele captura a maioria dos clientes que de fato cancelariam.
- A **precisão de apenas 54%** é a principal limitação quantitativa: de
  cada 10 clientes sinalizados como "em risco de churn", **menos de 6 de
  fato cancelariam** — os demais são falsos positivos. Qualquer ação de
  retenção automatizada a partir deste modelo deve assumir essa taxa de
  erro e ter custo baixo o suficiente para ser economicamente viável mesmo
  quando aplicada a clientes que não iriam cancelar.
- O **desvio-padrão do recall (±0,0378)** é o maior entre as métricas,
  indicando que a sensibilidade ao churn **varia mais entre diferentes
  recortes dos dados** do que as demais métricas — um sinal de que o
  desempenho de recall pode ser menos consistente em subpopulações não
  representadas de forma homogênea nos folds.

## Limitações

1. **Precisão moderada (54%) sob uma carga de teste grande**: mesmo
   avaliado de forma robusta (K-Fold, não um único split favorável), o
   modelo gera uma proporção relevante de falsos positivos. Não é adequado
   para decisões de alto custo por cliente sinalizado sem triagem humana
   complementar.
2. **Dataset estático e de origem única**: o modelo foi treinado sobre uma
   única base histórica (Telco Customer Churn, IBM), de um único mercado e
   um único momento no tempo. Não há garantia de que os padrões aprendidos
   se mantenham válidos para outra operadora, outra região ou outro
   período — especialmente diante de mudanças de portfólio de planos,
   preços ou comportamento de consumo (*data drift*).
3. **Ausência de dados temporais/sequenciais**: o modelo não captura
   tendências de uso ao longo do tempo (ex.: queda recente de consumo),
   apenas um retrato transversal (*snapshot*) do cliente — eventos recentes
   que antecedem o cancelamento podem não estar representados nas
   features disponíveis.
4. **Dependência de qualidade de dados de entrada**: campos ausentes ou
   inconsistentes (ex.: `TotalCharges` vazio para clientes novos) exigem
   tratamento de pré-processamento consistente entre treino e inferência;
   divergências nesse pipeline degradam a performance sem erro explícito.
5. **Interpretabilidade parcial**: por ser um ensemble de múltiplas
   árvores, o modelo não oferece uma explicação direta e auditável por
   predição individual (apenas importância de features agregada),
   limitando a explicabilidade caso-a-caso exigida em alguns contextos
   regulatórios.

## Viés e considerações éticas

- **Atributos sensíveis presentes nos dados de entrada**: a base contém
  `gender` (gênero) e `SeniorCitizen` (idoso), que são atributos
  potencialmente sensíveis sob a ótica de equidade algorítmica. O modelo
  **não foi submetido a uma auditoria formal de fairness** (ex.: paridade
  de recall/precisão entre grupos de gênero ou faixa etária) nesta versão
  — isso é uma lacuna conhecida, não uma garantia de ausência de viés.
- **Viés histórico herdado dos dados**: como qualquer modelo supervisionado,
  o Random Forest reproduz os padrões de churn presentes na base de
  treino. Se o histórico de cancelamentos refletir, por exemplo, diferenças
  estruturais de atendimento ou oferta entre perfis de clientes, o modelo
  pode perpetuar esse padrão em suas priorizações de retenção.
- **Risco de uso discriminatório indireto**: embora o modelo não utilize
  `gender`/`SeniorCitizen` como justificativa declarada de decisão, variáveis
  correlacionadas (ex.: tipo de plano, forma de pagamento) podem atuar como
  **proxies** desses atributos. Recomenda-se avaliação de correlação entre
  as features de maior importância e os atributos sensíveis antes de
  qualquer uso que impacte tratamento diferenciado de clientes.
- **Recomendação de uso responsável**: tratar a saída do modelo como um
  **indicador de priorização operacional** (quem contatar primeiro), nunca
  como critério de exclusão ou tratamento degradado de um cliente, e
  revisitar periodicamente a performance por subgrupo à medida que dados
  rotulados por grupo demográfico estiverem disponíveis para auditoria.

## Declaração de transparência

Este model card foi preenchido com base exclusivamente em evidência
empírica gerada pelo próprio pipeline de experimentação do projeto
(métricas de validação cruzada versionadas via DVC, análise comparativa
documentada em `docs/Por que o Random Forest para ser o modelo campeao`).
Nenhuma métrica de fairness por subgrupo demográfico foi calculada até o
momento da publicação deste card — essa é uma limitação assumida
explicitamente, e não uma alegação de neutralidade do modelo. Recomenda-se
que qualquer equipe que promova este modelo para um ambiente de maior
impacto (ex.: decisões com efeito financeiro direto sobre o cliente)
primeiro conduza uma auditoria de equidade dedicada e amplie a avaliação
para dados fora da distribuição de treino original.
