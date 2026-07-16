"""
__init__.py para o pacote src.web

Módulo principal do dashboard hospitalar em Streamlit.
"""

from .utils import (
    validar_dataframe,
    validar_faixa,
    formatar_moeda,
    formatar_percentual,
    calcular_taxa_ocupacao,
    calcular_tempo_medio_espera,
    calcular_giro_leitos,
    classificar_ocupacao,
    classificar_tempo_espera,
)

__version__ = "1.0.0"
__author__ = "Wellington de Lima Catarina"
__email__ = "lelolima806@gmail.com"

__all__ = [
    # Validações
    "validar_dataframe",
    "validar_faixa",
    # Formatação
    "formatar_moeda",
    "formatar_percentual",
    "calcular_taxa_ocupacao",
    "calcular_tempo_medio_espera",
    "calcular_giro_leitos",
    # Classificação
    "classificar_ocupacao",
    "classificar_tempo_espera",
]