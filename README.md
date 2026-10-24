# Tech Challenge — Churn Prediction

Escopo do sistema preditivo: [ML Canvas](docs/ml_canvas.md) · [página visual](docs/ml_canvas.html).

---

## 📖 A história por trás do projeto

### O problema

Uma operadora de telecomunicações perde, todo mês, uma fatia de clientes que
simplesmente cancelam o serviço (**churn**). Cada cancelamento representa
receita recorrente perdida — e, pior, a empresa só fica sabendo do problema
*depois* que o cliente já foi embora. Sem um sinal de alerta antecipado, toda
ação de retenção é reativa: desconto de última hora, ligação de recuperação,
ou simplesmente a perda silenciosa do cliente.

A pergunta que motivou este projeto foi simples: **é possível prever, com
antecedência e com dados que a empresa já possui (tempo de contrato, tipo de
plano, forma de pagamento, serviços contratados), quais clientes têm maior
probabilidade de cancelar?**

### A solução

Seguindo a metodologia **CRISP-DM**, o projeto percorreu todo o ciclo de um
produto de dados:

1. **Entendimento e preparação dos dados** — análise exploratória, tratamento
   de valores ausentes, engenharia de features (ex.: contagem de addons
   contratados, faixas de tempo de permanência) e balanceamento de classes.
2. **Modelagem comparativa** — cinco famílias de algoritmos foram treinadas,
   ajustadas e validadas por **K-Fold estratificado**: Regressão Logística,
   Árvore de Decisão, Random Forest, AdaBoost, Gradient Boosting e Redes
   Neurais (MLP). Todo o histórico de experimentos ficou versionado em
   `notebooks/*/historico/`, com métricas rastreadas via **DVC**
   (`dvc metrics show`).
3. **Escolha do modelo campeão** — entre os seis candidatos, o **Random
   Forest** venceu por equilibrar o maior poder de discriminação (ROC AUC),
   a melhor estabilidade entre folds (menor variância) e um recall alto o
   suficiente para não deixar passar batido o cliente que está de saída —
   sem sacrificar demais a precisão. O diagnóstico completo da escolha está
   documentado em `docs/Por que o Random Forest para ser o modelo campeao`.
4. **Produtização** — o modelo campeão foi encapsulado em uma **API REST
   (FastAPI)**, seguindo princípios de responsabilidade única, baixo
   acoplamento e o padrão de projeto **Factory** para a construção de todas
   as classes de configuração e serviço. A API conta com validação de
   entrada (Pydantic), tratamento padronizado de exceções, logging com
   mascaramento de dados sensíveis, **rate limiting** por cliente e
   **CORS** configurável — tudo isolado em um **container Docker**
   reprodutível em qualquer máquina.

### Os resultados

Métricas do modelo campeão (Random Forest), validadas por **K-Fold (5
folds)** sobre o conjunto de teste — a métrica mais confiável para avaliar
como o modelo generaliza para clientes que ele nunca viu:

| Métrica | Média (K-Fold) | Desvio padrão |
|---|---|---|
| **ROC AUC** | 0,8468 | ± 0,0109 |
| **Recall** (sensibilidade ao churn) | 0,7717 | ± 0,0378 |
| **F1-score** | 0,6348 | ± 0,0218 |
| **Acurácia** | 0,7657 | ± 0,0123 |
| **Precisão** | 0,5394 | ± 0,0159 |

Na prática, isso significa que o modelo **identifica corretamente ~77% dos
clientes que de fato cancelariam** — o indicador mais crítico para o
negócio, já que o custo de uma campanha de retenção desnecessária é muito
menor do que o custo de perder um cliente sem nenhum aviso prévio. O baixo
desvio padrão entre os folds (ROC AUC ±0,0109) também indica que o modelo é
**estável**: seu desempenho não depende de sorte em um recorte específico
dos dados, o que é um bom indício de resiliência a mudanças graduais no
perfil dos clientes (*data drift*) ao longo do tempo.

---

## 🧰 Pré-requisitos

Para instalar e executar o projeto (tanto o pipeline de dados/notebooks
quanto a API containerizada), você vai precisar de:

| Ferramenta | Uso no projeto | Observação |
|---|---|---|
| **Git** | Clonar o repositório | Qualquer versão recente |
| **[uv](https://docs.astral.sh/uv/)** | Gerenciador de dependências e ambientes Python do projeto | Instala o Python 3.14 automaticamente se necessário |
| **Python 3.14+** | Interpretador usado pelo projeto | Gerenciado pelo `uv`, não precisa instalar manualmente |
| **Docker** e **Docker Compose** | Build e execução da API em container | Necessário apenas para rodar a API containerizada |
| **DVC** | Versionamento de dados/modelos/métricas | Já incluído como dependência do grupo `notebooks` via `uv` |

Não é necessário instalar pip ou DVC manualmente: o `uv` resolve e
instala tudo a partir do `pyproject.toml`/`uv.lock`.

---

## 🚀 Instalação — do GitHub até a imagem Docker

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd Tech_Challenge_Churn_Prediction
```

### 2. Instalar as dependências do projeto (ambiente local)

```bash
uv sync
```

Isso instala as dependências de produção, desenvolvimento (testes, linter) e
notebooks (jupyter, dvc, matplotlib etc.) — suficiente para rodar os
notebooks, os testes e a API localmente fora do Docker, se desejar.

### 3. Configurar o arquivo `.env`

Todas as configurações da aplicação (título da API, nível de log, caminho
do modelo, limite de requisições, política de CORS etc.) são lidas
**exclusivamente de variáveis de ambiente** — não existe nenhum valor
hardcoded no código-fonte como fallback. Isso significa que **o `.env` é
obrigatório** para a aplicação iniciar.

```bash
cp .env.example .env
```

Em seguida, abra o `.env` e ajuste cada variável ao seu ambiente. O arquivo
`.env.example` documenta todas as variáveis necessárias com valores
**ilustrativos** (propositalmente diferentes dos valores reais usados em
produção, para não expor configuração sensível no repositório) — use-o como
referência de formato, não copie os valores literalmente. Dicas por grupo:

- **`APP_*`** — título e versão exibidos na documentação OpenAPI da API
  (`/docs`). Livre, não afeta o funcionamento.
- **`LOG_*`** — nível (`INFO`, `DEBUG`, `WARNING`...) e formato das mensagens
  de log. Use `DEBUG` em desenvolvimento e um nível mais alto em produção
  para reduzir ruído.
- **`MODEL_*`** — nome do diretório (`models`) e do arquivo `.joblib` do
  modelo campeão. Só altere se você treinou/salvou o modelo com outro nome
  de arquivo; o padrão já corresponde à estrutura deste repositório.
- **`SECURITY_*`** — lista (em JSON) dos campos do payload que devem ser
  mascarados nos logs, e o texto usado como máscara. Adicione aqui qualquer
  campo sensível do seu domínio antes de ir para produção.
- **`PREDICTION_*`** — limiar de probabilidade (entre 0 e 1) a partir do
  qual a predição é classificada como "churn". Valores mais baixos tornam o
  modelo mais sensível (mais alertas, mais falsos positivos); valores mais
  altos, mais conservador.
- **`RATE_LIMIT_*`** — quantidade de requisições permitidas por cliente,
  a janela de tempo (em segundos) dessa contagem, e o nome do cabeçalho HTTP
  usado para informar quantas requisições ainda restam. Ajuste conforme o
  tráfego esperado do seu ambiente.
- **`CORS_*`** — veja a seção dedicada abaixo, é a mais importante para
  garantir que a API funcione corretamente a partir de outra máquina/porta.

> ⚠️ **Nunca** faça commit do seu `.env` real — ele já está listado no
> `.gitignore`. Apenas o `.env.example` (com valores ilustrativos) deve ir
> para o repositório.

> 📌 **Nota de avaliação acadêmica**: para fins de avaliação da banca deste
> Tech Challenge, as variáveis em `.env.example` estão temporariamente
> preenchidas com os valores reais utilizados neste projeto, para facilitar
> a reprodução do ambiente durante a correção. Em commits futuros, esses
> valores serão revertidos para valores ilustrativos de exemplo.

### 4. Configurando o CORS para reprodutibilidade em qualquer máquina

O CORS (*Cross-Origin Resource Sharing*) controla **de quais origens**
(combinação exata de esquema + host + porta) um navegador tem permissão de
chamar a API. Se você rodar a API em uma máquina e tentar consumi-la a
partir de um front-end, Swagger UI externo ou outra ferramenta rodando em
uma origem diferente, o navegador **vai bloquear a requisição** até que essa
origem seja explicitamente liberada.

Para que o projeto funcione em qualquer máquina (não apenas na sua), ajuste
estas quatro variáveis no seu `.env`:

```env
CORS_ORIGENS_PERMITIDAS=["http://localhost:<porta-que-voce-vai-usar>"]
CORS_METODOS_PERMITIDOS=["GET","POST"]
CORS_CABECALHOS_PERMITIDOS=["*"]
CORS_PERMITIR_CREDENCIAIS="false"
```

Passo a passo para configurar corretamente:

1. **Identifique a origem real que vai consumir a API** — isto é, o
   endereço exatamente como aparece na barra do navegador (ou como o seu
   cliente HTTP está configurado) de onde as requisições partem. Exemplos:
   `http://localhost:3000` (um front-end local), `http://localhost:8001`
   (se você mesmo for testar via Swagger UI na mesma porta publicada pelo
   Docker) ou o domínio real de um front-end hospedado.
2. **Preencha `CORS_ORIGENS_PERMITIDAS`** com essa origem exata, em formato
   de lista JSON — pode conter mais de uma origem, separadas por vírgula,
   se precisar liberar mais de um client (ex.: ambiente de homologação e
   local ao mesmo tempo).
3. **Não inclua a porta interna do container (`8000`)** — o navegador
   enxerga a porta publicada no host (por padrão `8001`, conforme o
   `docker-compose.yml`), não a porta interna.
4. Mantenha `CORS_METODOS_PERMITIDOS` restrito a `GET` e `POST` (únicos
   métodos que a API expõe) e `CORS_PERMITIR_CREDENCIAIS="false"`, a menos
   que você tenha um motivo explícito para enviar cookies/tokens entre
   origens — manter esse valor em `false` é a opção mais segura por padrão.
5. Sempre que mudar a porta publicada no host (seção seguinte) ou o
   endereço do client, **atualize `CORS_ORIGENS_PERMITIDAS` de acordo** —
   são duas configurações independentes que precisam ficar coerentes entre
   si para a reprodutibilidade funcionar em qualquer máquina.

### 5. Construir a imagem Docker

```bash
docker compose build
```

Esse comando lê o `Dockerfile` (imagem base `python:3.14.8-slim-bookworm`,
com tag fixa — nunca `latest` — para builds reprodutíveis), instala apenas
as dependências de produção (`requirements.txt`, gerado a partir do
`pyproject.toml` via `uv export`) e copia somente o necessário para servir
a API (`src/`, `models/`), deixando notebooks, testes e dados de treino fora
da imagem final.

---

## ▶️ Executando o container com reprodutibilidade

Com o `.env` já configurado (passo 3 acima), suba o serviço com:

```bash
docker compose up -d
```

O `docker-compose.yml` carrega **todas** as variáveis de ambiente
dinamicamente do seu `.env` via `env_file` — nenhuma delas fica fixada na
imagem Docker. Isso é o que garante a reprodutibilidade: a mesma imagem,
rodada em qualquer máquina, se comporta de acordo com as variáveis que
**você** definiu no seu próprio `.env`, sem precisar reconstruir a imagem
para trocar configuração.

Para confirmar que o container subiu corretamente:

```bash
docker compose ps
```

O status deve aparecer como `healthy` (o `HEALTHCHECK` do compose valida
automaticamente os endpoints de liveness e readiness). Em seguida, teste a
API na porta publicada no host (por padrão `8001`, ajustável em
`docker-compose.yml` caso a porta já esteja em uso na sua máquina):

```bash
curl http://localhost:8001/health/liveness
curl http://localhost:8001/health/readiness
```

Para acompanhar os logs em tempo real (úteis para conferir o nível de log
definido em `LOG_NIVEL` e o mascaramento de dados sensíveis em ação):

```bash
docker compose logs -f
```

Para encerrar o ambiente:

```bash
docker compose down
```

A documentação interativa da API (Swagger UI) fica disponível em
`http://localhost:8001/docs` assim que o container estiver de pé.

---

## 🧪 Testando o endpoint `POST /predict`

Com o container de pé (seção anterior), use as informações abaixo para
reproduzir a chamada de predição em qualquer máquina.

| Item | Valor |
|---|---|
| **Verbo HTTP** | `POST` (outros verbos retornam `405`) |
| **URL** | `http://localhost:8001/predict` (porta publicada no host) |
| **Header obrigatório** | `Content-Type: application/json` |
| **Header opcional** | `Accept: application/json` |
| **Autenticação** | Nenhuma (não há token/API key) |
| **Corpo** | JSON com os 17 campos descritos abaixo (todos obrigatórios) |

> O header `Origin` **não** é necessário para `curl`/Postman. O CORS só é
> verificado por navegadores (ex.: Swagger UI em `http://localhost:8001/docs`),
> e exige que a origem esteja em `CORS_ORIGENS_PERMITIDAS` (veja a seção 4).

### Payload de exemplo

```json
{
  "cliente_em_idade_avancada": 0,
  "casado": "Yes",
  "meses_como_cliente": 2,
  "possui_servico_telefonico": "Yes",
  "possui_multiplas_linhas": "No",
  "possui_servico_de_internet": "Fiber optic",
  "possui_seguranca_online": "No",
  "possui_backup_online": "No",
  "possui_protecao_dispositivo": "No",
  "possui_suporte_tecnico_premium": "No",
  "possui_streaming_tv_terceiros": "No",
  "possui_streaming_filmes_terceiros": "No",
  "tipo_contrato": "Month-to-month",
  "fatura_sem_papel": "Yes",
  "metodo_pagamento": "Electronic check",
  "cobranca_mensal": 70.7,
  "total_cobrado_durante_trimestre": 151.65
}
```

### Valores aceitos por campo

| Campo | Tipo / valores válidos |
|---|---|
| `cliente_em_idade_avancada` | `0` ou `1` |
| `casado`, `possui_servico_telefonico`, `fatura_sem_papel` | `"Yes"`, `"No"` |
| `meses_como_cliente` | inteiro `>= 0` |
| `possui_multiplas_linhas` | `"Yes"`, `"No"`, `"No phone service"` |
| `possui_servico_de_internet` | `"DSL"`, `"Fiber optic"`, `"No"` |
| `possui_seguranca_online`, `possui_backup_online`, `possui_protecao_dispositivo`, `possui_suporte_tecnico_premium`, `possui_streaming_tv_terceiros`, `possui_streaming_filmes_terceiros` | `"Yes"`, `"No"`, `"No internet service"` |
| `tipo_contrato` | `"Month-to-month"`, `"One year"`, `"Two year"` |
| `metodo_pagamento` | `"Mailed check"`, `"Electronic check"`, `"Bank transfer (automatic)"`, `"Credit card (automatic)"` |
| `cobranca_mensal`, `total_cobrado_durante_trimestre` | número `>= 0` |

### curl (Linux/macOS/Git Bash)

```bash
curl -i -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "cliente_em_idade_avancada": 0,
    "casado": "Yes",
    "meses_como_cliente": 2,
    "possui_servico_telefonico": "Yes",
    "possui_multiplas_linhas": "No",
    "possui_servico_de_internet": "Fiber optic",
    "possui_seguranca_online": "No",
    "possui_backup_online": "No",
    "possui_protecao_dispositivo": "No",
    "possui_suporte_tecnico_premium": "No",
    "possui_streaming_tv_terceiros": "No",
    "possui_streaming_filmes_terceiros": "No",
    "tipo_contrato": "Month-to-month",
    "fatura_sem_papel": "Yes",
    "metodo_pagamento": "Electronic check",
    "cobranca_mensal": 70.7,
    "total_cobrado_durante_trimestre": 151.65
  }'
```

### PowerShell (Windows)

```powershell
$corpo = @{
  cliente_em_idade_avancada = 0
  casado = "Yes"
  meses_como_cliente = 2
  possui_servico_telefonico = "Yes"
  possui_multiplas_linhas = "No"
  possui_servico_de_internet = "Fiber optic"
  possui_seguranca_online = "No"
  possui_backup_online = "No"
  possui_protecao_dispositivo = "No"
  possui_suporte_tecnico_premium = "No"
  possui_streaming_tv_terceiros = "No"
  possui_streaming_filmes_terceiros = "No"
  tipo_contrato = "Month-to-month"
  fatura_sem_papel = "Yes"
  metodo_pagamento = "Electronic check"
  cobranca_mensal = 70.7
  total_cobrado_durante_trimestre = 151.65
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8001/predict" `
  -ContentType "application/json" -Body $corpo
```

### Resposta esperada (`200 OK`)

```json
{
  "churn_previsto": true,
  "probabilidade_churn": 0.0,
  "probabilidade_nao_churn": 0.0
}
```

Os valores de probabilidade acima são ilustrativos: o formato é fixo, mas os
números dependem do modelo versionado em `models/`. `churn_previsto` é `true`
quando `probabilidade_churn >= PREDICTION_LIMIAR_DECISAO_CHURN`. A resposta
inclui o header `X-RateLimit-Remaining` (nome definido em
`RATE_LIMIT_CABECALHO_REQUISICOES_RESTANTES`).

### Códigos de erro

Erros seguem o formato `{"level", "message", "erro", "cause"}`.

| Status | Quando ocorre |
|---|---|
| `400` | Falha no pré-processamento do payload |
| `405` | Verbo diferente de `POST` |
| `422` | Campo ausente, valor fora da lista aceita ou tipo inválido (validação do Pydantic) |
| `429` | Mais de `RATE_LIMIT_LIMITE_REQUISICOES` requisições por `RATE_LIMIT_JANELA_EM_SEGUNDOS` (por IP; padrão do `.env.example`: 10 por 60 s). Aguarde a janela expirar |
| `500` | Falha ao carregar o modelo ou executar a predição |

Exemplo de teste de validação (deve retornar `422`):

```bash
curl -i -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"casado": "Talvez"}'
```
