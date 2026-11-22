"""Teste de execução do ETL de dados sintéticos."""

import runpy
from pathlib import Path

ETL = Path(__file__).resolve().parents[1] / "src" / "etl" / "pacientes_etl.py"


def test_etl_cria_diretorio_e_csvs(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(ETL), run_name="__main__")
    for nome in ["pacientes", "internacoes", "medicos", "leitos"]:
        assert (tmp_path / "data" / f"{nome}_sample.csv").stat().st_size > 0
