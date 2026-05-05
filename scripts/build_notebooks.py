"""Gera notebooks de EDA e modelagem (executar: python scripts/build_notebooks.py)."""
from __future__ import annotations

import json
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parents[1]


def save(nb, name: str) -> None:
    p = ROOT / "notebooks" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print("OK", p)


def eda_notebook() -> None:
    cells = []
    cells.append(
        new_markdown_cell(
            """# EDA — NPS Preditivo (Fase 1)

Análise exploratória **orientada a negócio** sobre pedidos, logística e atendimento.

- **Alvo:** `nps_score` (0 a 10), coletado após a jornada.
- **Tríade NPS (0–10):** Detrator ≤6, Neutro 7–8, Promotor ≥9.

Os gráficos são gravados em `reports/` para uso nos slides."""
        )
    )
    cells.append(
        new_code_cell(
            r"""from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

_cwd = Path.cwd().resolve()
PROJECT_ROOT = _cwd if (_cwd / "data" / "raw" / "desafio_nps_fase_1.csv").exists() else _cwd.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "desafio_nps_fase_1.csv"
REPORTS = PROJECT_ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

assert RAW_PATH.exists(), f"CSV não encontrado: {RAW_PATH}"

pd.set_option("display.max_columns", None)
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.dpi"] = 120

df = pd.read_csv(RAW_PATH)

def nps_categoria(x: float) -> str:
    if x >= 9:
        return "Promotor"
    if x >= 7:
        return "Neutro"
    return "Detrator"

df["nps_categoria"] = df["nps_score"].map(nps_categoria)
df.head()"""
        )
    )
    cells.append(new_markdown_cell("## 1. Qualidade dos dados"))
    cells.append(
        new_code_cell(
            """print("Shape:", df.shape)
print("Duplicados order_id:", df["order_id"].duplicated().sum())
print("Nulos por coluna:")
print(df.isna().sum().sort_values(ascending=False).head(10))
df.info()"""
        )
    )
    cells.append(new_markdown_cell("## 2. Distribuição do NPS (nota 0–10)"))
    cells.append(
        new_code_cell(
            """fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(df["nps_score"], bins=21, kde=True, ax=ax, color="#2E86AB")
ax.set_title("Distribuição do NPS (nota)")
ax.set_xlabel("nps_score")
plt.tight_layout()
fig.savefig(REPORTS / "fig01_hist_nps.png", dpi=150, bbox_inches="tight")
plt.show()"""
        )
    )
    cells.append(
        new_code_cell(
            """order = ["Detrator", "Neutro", "Promotor"]
counts = df["nps_categoria"].value_counts().reindex(order)
fig, ax = plt.subplots(figsize=(6, 4))
counts.plot(kind="bar", ax=ax, color=["#C73E1D", "#F4A259", "#2A9D8F"])
ax.set_title("Volume por categoria NPS")
ax.set_ylabel("Pedidos")
plt.xticks(rotation=0)
plt.tight_layout()
fig.savefig(REPORTS / "fig02_categorias_nps.png", dpi=150, bbox_inches="tight")
plt.show()
counts"""
        )
    )
    cells.append(
        new_markdown_cell(
            """## 3. Logística: atraso é o fator mais crítico

O atraso na entrega apresenta associação forte com notas mais baixas (ver correlação no final). Aqui comparamos **média de NPS** por faixa de dias de atraso."""
        )
    )
    cells.append(
        new_code_cell(
            """bins = [-1, 0, 1, 3, 365]
labels = ["Sem atraso", "1 dia", "2 a 3 dias", "4+ dias"]
df["faixa_atraso"] = pd.cut(df["delivery_delay_days"], bins=bins, labels=labels)
tbl = df.groupby("faixa_atraso", observed=True)["nps_score"].agg(["mean", "median", "count"])
display(tbl)

fig, ax = plt.subplots(figsize=(8, 4))
# RdYlGn_r: verde = melhor (sem atraso), vermelho = pior (4+ dias)
sns.boxplot(
    data=df,
    x="faixa_atraso",
    y="nps_score",
    order=labels,
    hue="faixa_atraso",
    hue_order=labels,
    palette="RdYlGn_r",
    dodge=False,
    legend=False,
    ax=ax,
)
ax.set_title("NPS por faixa de atraso na entrega")
plt.xticks(rotation=15)
plt.tight_layout()
fig.savefig(REPORTS / "fig03_nps_por_atraso.png", dpi=150, bbox_inches="tight")
plt.show()"""
        )
    )
    cells.append(
        new_markdown_cell(
            """## 4. Reclamações e atendimento

Mais reclamações e mais contatos com atendimento costumam indicar **jornada problemática** e NPS menor."""
        )
    )
    cells.append(
        new_code_cell(
            """fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.lineplot(data=df, x="complaints_count", y="nps_score", err_style="band", marker="o", ax=axes[0], color="#6A4C93")
axes[0].set_title("NPS médio × número de reclamações")
sns.lineplot(data=df, x="customer_service_contacts", y="nps_score", err_style="band", marker="o", ax=axes[1], color="#1982C4")
axes[1].set_title("NPS médio × contatos com atendimento")
plt.tight_layout()
fig.savefig(REPORTS / "fig04_reclamacoes_atendimento.png", dpi=150, bbox_inches="tight")
plt.show()"""
        )
    )
    cells.append(new_markdown_cell("## 5. CSAT interno vs NPS declarado"))
    cells.append(
        new_code_cell(
            """fig, ax = plt.subplots(figsize=(6, 5))
sns.scatterplot(data=df, x="csat_internal_score", y="nps_score", alpha=0.35, ax=ax)
ax.set_title("CSAT interno vs NPS")
plt.tight_layout()
fig.savefig(REPORTS / "fig05_csat_vs_nps.png", dpi=150, bbox_inches="tight")
plt.show()

df[["nps_score", "csat_internal_score"]].corr()"""
        )
    )
    cells.append(new_markdown_cell("## 6. Região e tempo de relacionamento"))
    cells.append(
        new_code_cell(
            """fig, axes = plt.subplots(1, 2, figsize=(11, 4))
order_reg = sorted(df["customer_region"].unique())
sns.barplot(data=df, x="customer_region", y="nps_score", order=order_reg, ax=axes[0], errorbar="ci", palette="pastel")
axes[0].set_title("NPS médio por região")
axes[0].tick_params(axis="x", rotation=20)

df["tenure_bin"] = pd.qcut(df["customer_tenure_months"], q=4, duplicates="drop")
sns.barplot(data=df, x="tenure_bin", y="nps_score", ax=axes[1], errorbar="ci", palette="crest")
axes[1].set_title("NPS por quartil de tenure (meses)")
axes[1].tick_params(axis="x", rotation=35)
plt.tight_layout()
fig.savefig(REPORTS / "fig06_regiao_tenure.png", dpi=150, bbox_inches="tight")
plt.show()"""
        )
    )
    cells.append(new_markdown_cell("## 7. “Ponto de ruptura” na experiência"))
    cells.append(
        new_code_cell(
            """# Combinações operacionais críticas (linguagem para gestão)
df["ruptura_atraso"] = df["delivery_delay_days"] >= 4
df["ruptura_reclama"] = df["complaints_count"] >= 3

g = df.groupby(["ruptura_atraso", "ruptura_reclama"])["nps_score"].agg(["mean", "count"])
display(g.round(2))

fig, ax = plt.subplots(figsize=(7, 4))
plot_df = (
    df.assign(
        perfil=np.where(
            df["ruptura_atraso"] & df["ruptura_reclama"],
            "Atraso 4+ e 3+ reclamações",
            np.where(
                df["ruptura_atraso"],
                "Só atraso 4+ dias",
                np.where(df["ruptura_reclama"], "Só 3+ reclamações", "Demais pedidos"),
            ),
        )
    )
)
order_p = ["Demais pedidos", "Só 3+ reclamações", "Só atraso 4+ dias", "Atraso 4+ e 3+ reclamações"]
sns.barplot(data=plot_df, x="perfil", y="nps_score", order=order_p, ax=ax, palette="rocket")
ax.set_title("NPS médio por perfil de risco operacional")
plt.xticks(rotation=15, ha="right")
plt.tight_layout()
fig.savefig(REPORTS / "fig07_ponto_ruptura.png", dpi=150, bbox_inches="tight")
plt.show()"""
        )
    )
    cells.append(new_markdown_cell("## 8. Mapa de correlações (variáveis numéricas)"))
    cells.append(
        new_code_cell(
            """num = df.select_dtypes(include=[np.number]).drop(columns=["customer_id", "order_id"], errors="ignore")
corr = num.corr()
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corr, annot=False, cmap="vlag", center=0, ax=ax)
ax.set_title("Correlação entre variáveis numéricas")
plt.tight_layout()
fig.savefig(REPORTS / "fig08_heatmap_corr.png", dpi=150, bbox_inches="tight")
plt.show()

corr["nps_score"].drop("nps_score").sort_values(key=abs, ascending=False).head(12)"""
        )
    )
    cells.append(
        new_markdown_cell(
            """## 9. Síntese para storytelling (gestão)

- **Problema visível:** maioria dos pedidos cai como **detrator** na tríade 0–10; poucos promotores.
- **Atraso:** pedidos **sem atraso** têm NPS médio muito superior aos de **4+ dias** de atraso — é o principal “alavanca” operacional nesta base.
- **Reclamações / atendimento:** cada reclamação a mais e cada contato extra pressionam o NPS para baixo.
- **CSAT interno** acompanha o NPS (bom sinal de consistência dos indicadores internos).
- **Região:** diferenças entre regiões são **modestas** frente ao efeito de atraso e reclamações — priorizar **execução logística e qualidade** antes de campanhas regionais genéricas.

Exportamos a base enriquecida para `data/processed/` (também reproduzível via `python scripts/prepare_data.py`)."""
        )
    )
    cells.append(
        new_code_cell(
            """import subprocess
import sys

# Regenera CSV processado (mesma lógica que `python scripts/prepare_data.py`)
subprocess.check_call([sys.executable, str(PROJECT_ROOT / "scripts" / "prepare_data.py")], cwd=str(PROJECT_ROOT))
print("Base processada atualizada em data/processed/.")"""
        )
    )

    nb = new_notebook(cells=cells, metadata={"language_info": {"name": "python"}})
    save(nb, "01_eda_nps.ipynb")


def model_notebook() -> None:
    cells = []
    cells.append(
        new_markdown_cell(
            """# Modelo preditivo — NPS (opcional do desafio)

**Pergunta:** com dados operacionais disponíveis **antes** da pesquisa NPS, estimar a nota (regressão) e identificar pedidos em risco.

- **Alvo:** `nps_score` (regressão). Complemento: métricas de classificação binária **detrator** (nota < 7) para decisão operacional.
- **Entradas:** pedido, logística, atendimento (sem vazamento de informação futura). Excluímos `customer_id` e `order_id` do modelo.
- **Separação:** 80% treino / 20% teste, `random_state=42` (base transversal; em produção, validar por tempo).
- **Modelo:** `HistGradientBoostingRegressor` (bom padrão em dados tabulares heterogêneos).
- **Avaliação:** MAE, RMSE, R² no teste; importância de features.
- **Uso prático:** priorizar inspeção de pedidos com **NPS predito baixo** antes do envio da pesquisa; acionar logística/atendimento."""
        )
    )
    cells.append(
        new_code_cell(
            r"""from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

_cwd = Path.cwd().resolve()
PROJECT_ROOT = _cwd if (_cwd / "data" / "processed" / "dataset_processado.csv").exists() else _cwd.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "dataset_processado.csv"
MODELS = PROJECT_ROOT / "models"
REPORTS = PROJECT_ROOT / "reports"
MODELS.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

feature_cols = [
    "customer_age",
    "customer_region",
    "customer_tenure_months",
    "order_value",
    "items_quantity",
    "discount_value",
    "payment_installments",
    "delivery_time_days",
    "delivery_delay_days",
    "freight_value",
    "delivery_attempts",
    "customer_service_contacts",
    "resolution_time_days",
    "complaints_count",
    "repeat_purchase_30d",
    "csat_internal_score",
]
target = "nps_score"

X = df[feature_cols]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

categorical = ["customer_region"]
numeric = [c for c in feature_cols if c not in categorical]

preprocess = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ]
)

model = HistGradientBoostingRegressor(max_depth=6, learning_rate=0.06, max_iter=300, random_state=42)
pipe = Pipeline([("prep", preprocess), ("model", model)])
pipe.fit(X_train, y_train)

pred = pipe.predict(X_test)
mae = mean_absolute_error(y_test, pred)
rmse = root_mean_squared_error(y_test, pred)
r2 = r2_score(y_test, pred)
print(f"MAE: {mae:.3f} | RMSE: {rmse:.3f} | R2: {r2:.3f}")

# Classificação derivada: detrator < 7
y_bin = (y_test < 7).astype(int)
pred_bin = (pred < 7).astype(int)
acc = (y_bin == pred_bin).mean()
print(f"Acurácia detrator<7 (proxy): {acc:.3f}")

joblib.dump(pipe, MODELS / "pipeline_nps_hgb.joblib")
print("Modelo salvo em models/pipeline_nps_hgb.joblib")"""
        )
    )
    cells.append(
        new_code_cell(
            """# Importância por permutação (no conjunto de teste)
r = permutation_importance(pipe, X_test, y_test, n_repeats=15, random_state=42, n_jobs=-1)
# importances_mean tem o mesmo comprimento que colunas de X (pré-transformação)
imp = pd.Series(r.importances_mean, index=X_test.columns).sort_values(ascending=False).head(15)

fig, ax = plt.subplots(figsize=(8, 5))
imp.sort_values().plot.barh(ax=ax, color="#264653")
ax.set_title("Top features — importância por permutação")
plt.tight_layout()
fig.savefig(REPORTS / "fig09_importancia_modelo.png", dpi=150, bbox_inches="tight")
plt.show()"""
        )
    )
    cells.append(
        new_code_cell(
            """# Predito vs real (teste)
fig, ax = plt.subplots(figsize=(5, 5))
ax.scatter(y_test, pred, alpha=0.3, s=12)
lims = 0, 10
ax.plot(lims, lims, "r--", lw=1)
ax.set_xlim(lims)
ax.set_ylim(lims)
ax.set_xlabel("NPS real")
ax.set_ylabel("NPS predito")
ax.set_title("Teste: predito vs real")
plt.tight_layout()
fig.savefig(REPORTS / "fig10_pred_vs_real.png", dpi=150, bbox_inches="tight")
plt.show()"""
        )
    )

    nb = new_notebook(cells=cells, metadata={"language_info": {"name": "python"}})
    save(nb, "02_modelo_nps.ipynb")


def main() -> None:
    eda_notebook()
    model_notebook()


if __name__ == "__main__":
    main()
