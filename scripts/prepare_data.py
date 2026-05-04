"""
Tratamento e enriquecimento da base bruta.
Gera data/processed/dataset_processado.csv (reproduzível).
"""
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW = PROJECT_ROOT / "data" / "raw" / "desafio_nps_fase_1.csv"
OUT = PROJECT_ROOT / "data" / "processed" / "dataset_processado.csv"


def nps_categoria(score: float) -> str:
    if score >= 9:
        return "Promotor"
    if score >= 7:
        return "Neutro"
    return "Detrator"


def main() -> None:
    df = pd.read_csv(RAW)
    assert not df["order_id"].duplicated().any(), "Existem order_id duplicados."
    assert df.isna().sum().sum() == 0, "Existem valores ausentes a tratar."

    df["nps_categoria"] = df["nps_score"].map(nps_categoria)
    df["atraso_alto"] = (df["delivery_delay_days"] > 3).astype(int)
    df["reclama_alto"] = (df["complaints_count"] >= 3).astype(int)
    df["contato_atendimento"] = (df["customer_service_contacts"] > 0).astype(int)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Gravado: {OUT}  shape={df.shape}")


if __name__ == "__main__":
    main()
