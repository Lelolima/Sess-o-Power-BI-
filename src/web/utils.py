"""
Utilitários e helpers para o Dashboard Hospitalar.

Funções compartilhadas, validações e utilitários gerais.
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, Union
from datetime import datetime


# ============================================================================
# VALIDAÇÕES
# ============================================================================

def validar_dataframe(df: pd.DataFrame, colunas_obrigatorias: list[str]) -> bool:
    """
    Valida se DataFrame tem colunas obrigatórias.

    Args:
        df: DataFrame para validar
        colunas_obrigatorias: Lista de nomes de colunas requeridas

    Returns:
        True se válido, False caso contrário
    """
    if df is None or df.empty:
        return False

    colunas_existentes = set(df.columns)
    return all(col in colunas_existentes for col in colunas_obrigatorias)


def validar_faixa(valor: float, minimo: float, maximo: float) -> bool:
    """
    Valida se valor está dentro de faixa permitida.

    Args:
        valor: Valor numérico para validar
        minimo: Valor mínimo permitido
        maximo: Valor máximo permitido

    Returns:
        True se dentro da faixa, False caso contrário
    """
    return minimo <= valor <= maximo


# ============================================================================
# FORMATADORES
# ============================================================================

def formatar_moeda(valor: float, simbolo: str = "R$") -> str:
    """
    Formata valor como moeda brasileira.

    Args:
        valor: Valor numérico
        simbolo: Símbolo da moeda

    Returns:
        String formatada como moeda
    """
    return f"{simbolo} {valor:,.2f}"


def formatar_percentual(valor: float, casas_decimais: int = 1) -> str:
    """
    Formata valor como percentual.

    Args:
        valor: Valor numérico (0-100)
        casas_decimais: Número de casas decimais

    Returns:
        String formatada com símbolo de percentual
    """
    return f"{valor:.{casas_decimais}f}%"


def formatar_numero(valor: float, separador_milhar: str = ".") -> str:
    """
    Formata número com separador de milhar.

    Args:
        valor: Valor numérico
        separador_milhar: Caractere para separar milhares

    Returns:
        String formatada
    """
    return f"{int(valor):{separador_milhar}}"


# ============================================================================
# CÁLCULOS DE NEGÓCIO
# ============================================================================

def calcular_taxa_ocupacao(leitos_ocupados: int, total_leitos: int) -> float:
    """
    Calcula taxa de ocupação de leitos.

    Args:
        leitos_ocupados: Número de leitos ocupados
        total_leitos: Número total de leitos disponíveis

    Returns:
        Taxa de ocupação em percentual (0-100)
    """
    if total_leitos == 0:
        return 0.0

    return (leitos_ocupados / total_leitos) * 100


def calcular_tempo_medio_espera(valores: list[float]) -> float:
    """
    Calcula tempo médio de espera.

    Args:
        valores: Lista de tempos de espera em horas

    Returns:
        Tempo médio em horas
    """
    if not valores:
        return 0.0

    return np.mean(valores)


def calcular_giro_leitos(total_internacoes: int, total_leitos: int) -> float:
    """
    Calcula giro de leitos (internações por leito).

    Args:
        total_internacoes: Número total de internações no período
        total_leitos: Número total de leitos

    Returns:
        Giro de leitos
    """
    if total_leitos == 0:
        return 0.0

    return total_internacoes / total_leitos


def calcular_variação(valor_atual: float, valor_anterior: float) -> float:
    """
    Calcula variação percentual entre dois valores.

    Args:
        valor_atual: Valor do período atual
        valor_anterior: Valor do período anterior

    Returns:
        Variação percentual
    """
    if valor_anterior == 0:
        return 0.0

    return ((valor_atual - valor_anterior) / valor_anterior) * 100


# ============================================================================
# CLASSIFICADORES
# ============================================================================

def classificar_ocupacao(taxa: float) -> Dict[str, Any]:
    """
    Classifica taxa de ocupação por faixa.

    Args:
        taxa: Taxa de ocupação em percentual

    Returns:
        Dict com classificação, cor e ícone
    """
    if taxa < 70:
        return {
            "classificacao": "Baixa",
            "cor": "#2d8a2d",
            "icone": "🟢",
            "mensagem": "Ocupação dentro do ideal"
        }
    elif taxa < 85:
        return {
            "classificacao": "Normal",
            "cor": "#2d8a2d",
            "icone": "🟢",
            "mensagem": "Ocupação normal"
        }
    elif taxa < 90:
        return {
            "classificacao": "Atenção",
            "cor": "#ffa502",
            "icone": "🟡",
            "mensagem": "Ocupação elevada - monitore"
        }
    elif taxa < 95:
        return {
            "classificacao": "Crítica",
            "cor": "#ff6b6b",
            "icone": "🟠",
            "mensagem": "Ocupação crítica - ações necessárias"
        }
    else:
        return {
            "classificacao": "Colapso",
            "cor": "#d92d2d",
            "icone": "🔴",
            "mensagem": "Capacidade máxima atingida"
        }


def classificar_tempo_espera(horas: float) -> Dict[str, Any]:
    """
    Classifica tempo médio de espera.

    Args:
        horas: Tempo em horas

    Returns:
        Dict com classificação e status
    """
    if horas < 2:
        return {"classificacao": "Excelente", "cor": "#2d8a2d", "icone": "✅"}
    elif horas < 4:
        return {"classificacao": "Bom", "cor": "#2d8a2d", "icone": "👍"}
    elif horas < 6:
        return {"classificacao": "Regular", "cor": "#ffa502", "icone": "⚠️"}
    elif horas < 8:
        return {"classificacao": "Ruim", "cor": "#ff6b6b", "icone": "❌"}
    else:
        return {"classificacao": "Crítico", "cor": "#d92d2d", "icone": "🚨"}


# ============================================================================
# GERADORES DE DADOS (PARA TESTES)
# ============================================================================

def gerar_dados_sinteticos(
    num_dias: int = 365,
    data_inicio: str = '2024-01-01',
    seed: int = 42
) -> pd.DataFrame:
    """
    Gera dados sintéticos para testes e demonstração.

    Args:
        num_dias: Número de dias para gerar
        data_inicio: Data inicial
        seed: Seed para reproducibilidade

    Returns:
        DataFrame com dados sintéticos
    """
    np.random.seed(seed)

    datas = pd.date_range(data_inicio, periods=num_dias, freq='D')

    # Ocupação com sazonalidade
    base = 82 + 5 * np.sin(np.arange(num_dias) * 2 * np.pi / 365)
    ocupacao = np.clip(base + np.random.normal(0, 5, num_dias), 50, 98)

    return pd.DataFrame({
        'Data': datas,
        'Ocupacao': ocupacao,
        'Leitos_Disponiveis': np.random.randint(180, 220, num_dias),
    })