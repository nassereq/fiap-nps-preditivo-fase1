# Tech Challenge Fase 1 — Case NPS Preditivo

**Repositório público:** https://github.com/nassereq/fiap-nps-preditivo-fase1

Repositório pronto para entrega: **tratamento da base**, **EDA orientada a negócio**, **modelo preditivo opcional** (implementado), **documentação escrita**, **slides base** (PPTX) e **roteiro de vídeo**.

## Objetivo do projeto

Entender **o que move o NPS** em um e-commerce a partir de dados de pedido, logística e atendimento; comunicar insights a gestores; e (opcional no enunciado, **entregue aqui**) construir um **modelo em Python** que estima o `nps_score` antes da pesquisa, para priorização operacional.

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
| `reports/` | PNGs da EDA e do modelo + PPTX base da apresentação. |
| `models/` | `pipeline_nps_hgb.joblib` (treinado ao executar o notebook 02). |
| `docs/MEMORIA_ENTREGA.md` | Respostas aos itens 1, 2, 3 (síntese) e 4 do desafio. |
| `docs/ROTEIRO_VIDEO.md` | Roteiro sugerido para o vídeo de até 5 minutos. |

## Base de dados

- **Arquivo bruto:** `data/raw/desafio_nps_fase_1.csv` (~2.500 linhas, 19 colunas originais).
- **Variável-alvo:** `nps_score` (0 a 10).
- **Processado:** `dataset_processado.csv` inclui colunas auxiliares: `nps_categoria`, `atraso_alto`, `reclama_alto`, `contato_atendimento`.

## Metodologia (resumo)

1. **Qualidade:** ausência de nulos; `order_id` único (`scripts/prepare_data.py`).
2. **EDA:** distribuição do NPS, tríade Detrator/Neutro/Promotor, atraso, reclamações, atendimento, CSAT interno, região/tenure, “ponto de ruptura”, correlações — ver `docs/MEMORIA_ENTREGA.md`.
3. **Modelagem:** `HistGradientBoostingRegressor` em `Pipeline` com `ColumnTransformer` (numéricas + região em one-hot); hold-out 80/20; MAE, RMSE, R²; importância por permutação; artefato em `models/`.

## Como reproduzir (Windows / PowerShell)

```powershell
cd "c:\Users\capis\OneDrive\Área de Trabalho\FIAP\Preditivo-Cursor"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 1) Base processada
python scripts\prepare_data.py

# 2) EDA (gera PNGs em reports/)
jupyter nbconvert --to notebook --execute notebooks\01_eda_nps.ipynb --inplace

# 3) Modelo (gera/atualiza joblib e figuras 09–10)
jupyter nbconvert --to notebook --execute notebooks\02_modelo_nps.ipynb --inplace

# 4) Slides PowerPoint (texto executivo; insira as figuras de reports/ se desejar)
python scripts\gerar_slides.py
```

Para desenvolvimento interativo: `jupyter notebook notebooks\01_eda_nps.ipynb`.

## Entregas do desafio (checklist)

- [x] Repositório com tratamento, EDA, modelo e pipeline.
- [x] README com objetivo, dados, metodologia e reprodução.
- [x] Documentação escrita (`docs/MEMORIA_ENTREGA.md`).
- [x] Material de slides (`reports/Apresentacao_NPS_Fase1.pptx`) + figuras em `reports/`.
- [ ] **Vídeo (até 5 min):** gravar conforme `docs/ROTEIRO_VIDEO.md` (não automatizável no repositório).
- [ ] **GitHub público:** criar repositório, `git init`, commit e publicar o link na plataforma FIAP.

### Dica para os slides finais

Abra o `.pptx` e **insira** os arquivos `fig01_*.png` … `fig10_*.png` nos slides correspondentes (visual forte para gestores).

## Requisitos

Ver `requirements.txt` (pandas, numpy, matplotlib, seaborn, scikit-learn ≥ 1.4, jupyter, nbformat, joblib, python-pptx).

## Licença / uso

Projeto acadêmico FIAP — uso educacional.
