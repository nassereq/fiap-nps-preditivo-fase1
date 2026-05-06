# Tech Challenge Fase 1 — Case NPS Preditivo

**Repositório público:** https://github.com/nassereq/Tech_Challenge---Fase_1---Raphael_Reis

Projeto de entrega: **tratamento da base**, **EDA orientada a negócio**, **modelo preditivo** (implementado), **documentação escrita**, **slides** e **roteiros para vídeo**.

## Objetivo do projeto

Entender **o que move o NPS** em um e-commerce a partir de dados de pedido, logística e atendimento; comunicar insights a gestores; e construir um **modelo em Python** que estima o `nps_score` antes da pesquisa, para priorização operacional.

## Estrutura de pastas

| Caminho | Conteúdo |
|---------|-----------|
| `data/raw/` | CSV original (`desafio_nps_fase_1.csv`). |
| `data/processed/` | Base enriquecida (`dataset_processado.csv`) gerada pelo script de preparação. |
| `notebooks/01_eda_nps.ipynb` | EDA completa; grava figuras em `reports/`. |
| `notebooks/02_modelo_nps.ipynb` | Pipeline de ML + métricas + importância por permutação. |
| `scripts/prepare_data.py` | Validação, features derivadas e export do CSV processado. |
| `scripts/build_notebooks.py` | Regenera os notebooks a partir de templates em Python (opcional). |
| `scripts/gerar_slides.py` | Gera `reports/Apresentacao_NPS_Fase1.pptx`. |
| `reports/` | PNGs da EDA e do modelo |
| `models/` | `pipeline_nps_hgb.joblib` (treinado ao executar o notebook 02). |
| `docs/MEMORIA_ENTREGA.md` | Respostas aos itens 1, 2, 3 (síntese) e 4 do desafio. |
| `docs/ROTEIRO_VIDEO.md` | Roteiro genérico para vídeo (até 5 min). |
| `docs/ROTEIRO_VIDEO_FINAL.md` | Roteiro alinhado aos slides revisados (ensaio executivo). |

## Base de dados

- **Arquivo bruto:** `data/raw/desafio_nps_fase_1.csv` (~2.500 linhas, 19 colunas originais).
- **Variável-alvo:** `nps_score` (0 a 10).
- **Processado:** `dataset_processado.csv` inclui colunas auxiliares: `nps_categoria`, `atraso_alto`, `reclama_alto`, `contato_atendimento`.

## Metodologia (resumo)

1. **Qualidade:** ausência de nulos; `order_id` único (`scripts/prepare_data.py`).
2. **EDA:** distribuição do NPS, tríade Detrator/Neutro/Promotor, atraso, reclamações, atendimento, CSAT interno, região/tenure, “ponto de ruptura”, correlações — ver `docs/MEMORIA_ENTREGA.md`.
3. **Modelagem:** `HistGradientBoostingRegressor` em `Pipeline` com `ColumnTransformer` (numéricas + região em one-hot); hold-out 80/20; MAE, RMSE, R²; importância por permutação; artefato em `models/`.

## Obter o código

Clone o repositório e entre na pasta do projeto (nome da pasta = nome do repo):

```bash
git clone https://github.com/nassereq/Tech_Challenge---Fase_1---Raphael_Reis.git
cd Tech_Challenge---Fase_1---Raphael_Reis
```

*(Se estiver a trabalhar a partir de um ZIP da FIAP, descompacte e use `cd` para a pasta raiz onde estão `README.md`, `data/` e `notebooks/`.)*

## Como reproduzir

### Windows (PowerShell)

Na **raiz do repositório** (após o `cd` acima):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python scripts\prepare_data.py

jupyter nbconvert --to notebook --execute notebooks\01_eda_nps.ipynb --inplace
jupyter nbconvert --to notebook --execute notebooks\02_modelo_nps.ipynb --inplace

python scripts\gerar_slides.py
```

### Linux ou macOS (bash/zsh)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/prepare_data.py

jupyter nbconvert --to notebook --execute notebooks/01_eda_nps.ipynb --inplace
jupyter nbconvert --to notebook --execute notebooks/02_modelo_nps.ipynb --inplace

python scripts/gerar_slides.py
```

Para desenvolvimento interativo: `jupyter notebook` ou JupyterLab, abrindo os ficheiros em `notebooks/`.

## Entrega académica (checklist)

- [x] Código e dados tratados no GitHub público (link no topo).
- [x] README com objetivo, dados, metodologia e instruções de reprodução **sem caminhos absolutos da máquina**.
- [x] Documentação escrita do case (`docs/MEMORIA_ENTREGA.md`).
- [x] Slides e figuras em `reports/` (use a versão final do `.pptx` que submeter à FIAP).
- [ ] Vídeo executivo (≤ 5 min), conforme `docs/ROTEIRO_VIDEO_FINAL.md` ou `docs/ROTEIRO_VIDEO.md`.
- [ ] Submeter na plataforma FIAP: **URL do repositório** + ficheiros pedidos (vídeo/slides), conforme orientação da disciplina.

### Dica visual para os slides

Inserir nos slides os PNG `fig01` … `fig10` de `reports/` onde fizer sentido na narrativa (atraso, ruptura, modelo, etc.).

## Requisitos

Ver `requirements.txt` (pandas, numpy, matplotlib, seaborn, scikit-learn ≥ 1.4, jupyter, nbformat, joblib, python-pptx).

## Licença / uso

Projeto acadêmico FIAP — uso educacional.
