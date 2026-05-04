# Memória de entrega — Tech Challenge Fase 1 (NPS Preditivo)

Documento complementar ao repositório: respostas objetivas aos itens **1**, **2**, **3** (síntese) e **4** do enunciado. A análise detalhada está em `notebooks/01_eda_nps.ipynb`; o modelo opcional em `notebooks/02_modelo_nps.ipynb`.

---

## 1. Entendimento do negócio

### Qual problema de negócio está sendo resolvido?

O e-commerce cresceu em volume, mas o **NPS varia muito** entre clientes com indicadores operacionais aparentemente parecidos. O negócio não consegue **antecipar** insatisfação: o NPS só é medido **depois** da jornada, o que atrasa ações corretivas em logística, atendimento e produto. O problema é **priorizar onde agir antes da pesquisa**, usando dados de pedido, entrega e atendimento como sinais de risco de baixa recomendação.

### Por que o NPS é importante para um e-commerce?

O NPS resume a **propensão a recomendar** a marca. Em e-commerce, recomendação influencia **aquisição orgânica** (menos CAC), **confiança** em categorias sensíveis e **retenção**. Quedas de NPS costumam preceder aumento de churn, pressão em SAC e maior sensibilidade a preço.

### Quais áreas poderiam se beneficiar desses insights?

| Área | Uso dos insights |
|------|------------------|
| **Logística** | Reduzir atraso, tentativas falhas e variabilidade de prazo. |
| **Atendimento / SAC** | Priorizar filas quando há muitas reclamações ou tempo de resolução alto. |
| **Produto / UX** | Ajustar jornada de checkout, frete e expectativa de entrega. |
| **Pricing / Revenue** | Entender se descontos agressivos correlacionam com expectativas frágeis (avaliar com cautela). |
| **Estratégia / CX** | Metas de experiência, investimento em SLAs e comunicação proativa. |

### Reflexão: como o NPS impacta recompra, boca a boca e market share?

- **Recompra:** clientes promotores tendem a voltar; detratores abandonam ou compram só com promoção — o próprio dataset mostra **correlação positiva** entre `repeat_purchase_30d` e `nps_score`.
- **Boca a boca:** NPS é proxy de advocacy; detratores geram **custo reputacional** (reviews, redes).
- **Market share:** em mercados competitivos, experiência ruim reduz share **sem** que o preço mude — o cliente migra para concorrentes com entrega/atendimento mais previsíveis.

### Indicadores de mercado que complementariam

Benchmarks de NPS por vertical; **OTD/OTIF** (entrega no prazo / completa); **SLA de first response** do SAC; **taxa de devolução**; **NPS de concorrentes** (estudos de mercado); **CSAT por canal**; **tempo médio de entrega** por transportadora.

---

## 2. Definição da target (conceitual)

### Qual variável representa a satisfação do cliente?

A variável **`nps_score`** (nota de 0 a 10), coletada **após** a experiência de compra, conforme o dicionário de dados.

### Por que ela foi escolhida?

É o **indicador-alinhado ao case** e comunicável à liderança; permite a tríade clássica **Detrator / Neutro / Promotor** (≤6 / 7–8 / ≥9 em escala 0–10).

### Em que momento da jornada é coletada?

**Ao fim da jornada** (pós-entrega / pós-atendimento daquele pedido, conforme narrativa do desafio). Ou seja, é uma medida **lag** — não está disponível no meio da operação, daí o valor de um modelo **preditivo** com dados operacionais anteriores.

### Riscos de uso inadequado

- **Confundir correlação com causa** (ex.: atraso alto e NPS baixo podem ter causas comuns não observadas).
- **Viés de resposta** (só quem responde à pesquisa).
- **Uso indevido de CSAT interno** (`csat_internal_score`) em modelos de “antecipação” se ele for medido **no mesmo momento** que o NPS — na base atual tratamos como feature operacional correlata; em produção seria necessário **garantir temporalidade** (CSAT antes do NPS).
- **Alvos operacionais distorcem comportamento** (gamificação do indicador).

---

## 3. Análise exploratória — síntese para gestão

*(Detalhes e gráficos: `notebooks/01_eda_nps.ipynb` e imagens em `reports/`.)*

- **Distribuição:** a média de `nps_score` situa-se em torno de **4,4** em 2.500 pedidos; há **muitos detrators** e poucos promotores na tríade 0–10.
- **Fatores mais críticos:** **atraso na entrega** (`delivery_delay_days`) e **reclamações** (`complaints_count`) são os que mais “puxam” o NPS para baixo; **contatos com atendimento** também acompanham queda.
- **O que mais gera detratores:** combinação de **atraso elevado (4+ dias)** e **múltiplas reclamações** — perfil de “ruptura” claro nos gráficos de segmentação.
- **Ponto de ruptura:** pedidos **sem atraso** têm NPS médio **muito superior** aos pedidos com **4+ dias** de atraso; após certo nível de reclamações, o NPS médio cai de forma consistente.
- **Perfil de cliente:** diferenças entre **regiões** são **modestas** frente aos efeitos operacionais; **tenure** em quartis não domina a história — o foco deve ser **execução**, não campanha regional genérica.
- **CSAT interno** caminha junto com o NPS — útil como **sinal interno** de consistência.

---

## 4. Modelagem preditiva e uso de IA (reflexão + o que foi feito)

### Regressão vs classificação

| Abordagem | Prós | Contras |
|-----------|------|---------|
| **Regressão** (prever nota 0–10) | Informação fina, priorização por “risco contínuo”. | Erros de interpretação se gestores tratarem decimais como “precisão falsa”. |
| **Classificação** (ex.: detrator vs não) | Alinha-se a **ações binárias** (priorizar SAC / logística). | Perde nuances entre notas 3 e 6. |

**Estratégia adotada:** **regressão** com `HistGradientBoostingRegressor` como modelo principal (bom desempenho em tabelas heterogêneas) **e** leitura operacional via **proxy binário** detrator (`nps_score` < 7) para comunicação com negócio.

### Justificativa de negócio

Permite **fila de risco** de pedidos antes da pesquisa NPS, direcionando **contato proativo**, **upgrade de entrega** ou **escalonamento logístico**.

### Justificativa técnica

Pipeline com **One-Hot** para região e **pass-through** numérico; validação **hold-out 80/20**; métricas **MAE / RMSE / R²**; **importância por permutação** para explicabilidade operacional.

### Implementação (opcional entregue)

Ver `notebooks/02_modelo_nps.ipynb` e artefato `models/pipeline_nps_hgb.joblib`.

### Como a empresa usaria na prática

1. **Score diário** de pedidos concluídos com NPS ainda não respondido.  
2. **Alerta** para os 10% piores preditos → time logístico / SAC.  
3. **Revisão semanal** das variáveis mais importantes (atraso, reclamações) para **OKRs** de operação.

---

## Limitações e riscos (transparência)

- Dados **transversais**: não provam causalidade nem substituem experimentos (A/B, pilotos logísticos).
- **Generalização temporal:** padrões podem mudar (pandemia, greve, pico sazonal).
- **Governança:** modelo não deve **punir** clientes nem colaboradores sem processo humano.
- **Qualidade de dados:** reclamações mal classificadas distorcem o sinal.

---

## Recomendações práticas priorizadas

1. **Endurecer SLA de atraso** e plano de ação quando **atraso ≥ 4 dias** (comunicação proativa + compensação).  
2. **Quebrar o ciclo de reclamações:** root-cause em defeito, embalagem, transportadora e promessa de prazo.  
3. **Reduzir necessidade de contato** (autosserviço, rastreio, previsão de entrega).  
4. **Pilotar uso do score preditivo** em uma região ou categoria antes do rollout nacional.
