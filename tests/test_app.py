"""Smoke tests do app Streamlit usando streamlit.testing (executa o app de verdade)."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "src" / "web" / "app.py")
PAGINAS = ["Visão Geral", "Análise por Especialidade", "Custos e Faturamento", "Sobre"]


@pytest.mark.parametrize("pagina", PAGINAS)
def test_paginas_renderizam_sem_excecao(pagina):
    at = AppTest.from_file(APP, default_timeout=60).run()
    assert not at.exception
    at.sidebar.radio[0].set_value(pagina).run()
    assert not at.exception


def test_kpis_sao_deterministicos():
    """Os KPIs não podem mudar entre renderizações (antes eram np.random)."""
    a = AppTest.from_file(APP, default_timeout=60).run()
    b = AppTest.from_file(APP, default_timeout=60).run()
    assert [m.value for m in a.metric] == [m.value for m in b.metric]
    assert len(a.metric) >= 4


def test_calcular_kpis_operacionais():
    import pandas as pd

    from src.web.app import MESES, calcular_kpis_operacionais

    ocupacao = pd.DataFrame({"Leitos_Disponiveis": [200, 200]})
    esp = pd.DataFrame({
        "Mes": [MESES[-2], MESES[-1], MESES[-1]],
        "Pacientes": [200, 300, 100],
        "Tempo_Espera": [6.0, 2.0, 4.0],
    })
    k = calcular_kpis_operacionais(ocupacao, esp)
    assert k["giro_leitos"] == pytest.approx(2.0)
    assert k["delta_giro"] == pytest.approx(1.0)
    assert k["tempo_espera"] == pytest.approx(3.0)
    assert k["tempo_espera_medio"] == pytest.approx(4.0)
