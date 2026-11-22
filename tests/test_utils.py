"""
Testes unitários para utilitários do Dashboard Hospitalar.

Executar: pytest tests/test_utils.py -v
"""

import pandas as pd

from src.web.utils import (
    validar_dataframe,
    validar_faixa,
    formatar_moeda,
    formatar_percentual,
    formatar_numero,
    calcular_taxa_ocupacao,
    calcular_tempo_medio_espera,
    calcular_giro_leitos,
    calcular_variacao,
    classificar_ocupacao,
    classificar_tempo_espera,
    gerar_dados_sinteticos,
)


# =============================================================================
# TESTES DE VALIDAÇÃO
# =============================================================================

class TestValidacao:
    """Testes para funções de validação."""

    def test_validar_dataframe_vazio(self):
        """Deve retornar False para DataFrame vazio."""
        df = pd.DataFrame()
        assert validar_dataframe(df, ['coluna']) is False

    def test_validar_dataframe_none(self):
        """Deve retornar False para None."""
        assert validar_dataframe(None, ['coluna']) is False

    def test_validar_dataframe_colunas_faltantes(self):
        """Deve retornar False se colunas obrigatórias faltam."""
        df = pd.DataFrame({'A': [1, 2, 3]})
        assert validar_dataframe(df, ['A', 'B']) is False

    def test_validar_dataframe_valido(self):
        """Deve retornar True para DataFrame válido."""
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        assert validar_dataframe(df, ['A', 'B']) is True

    def test_validar_faixa_dentro(self):
        """Deve retornar True para valor dentro da faixa."""
        assert validar_faixa(50, 0, 100) is True

    def test_validar_faixa_fora(self):
        """Deve retornar False para valor fora da faixa."""
        assert validar_faixa(150, 0, 100) is False

    def test_validar_faixa_limite(self):
        """Deve incluir limites."""
        assert validar_faixa(0, 0, 100) is True
        assert validar_faixa(100, 0, 100) is True


# =============================================================================
# TESTES DE FORMATAÇÃO
# =============================================================================

class TestFormatacao:
    """Testes para funções de formatação."""

    def test_formatar_moeda(self):
        """Deve formatar valor como moeda brasileira."""
        assert formatar_moeda(1000.50) == "R$ 1,000.50"

    def test_formatar_moeda_simbolo_customizado(self):
        """Deve usar símbolo customizado."""
        assert formatar_moeda(1000.50, "$") == "$ 1,000.50"

    def test_formatar_percentual(self):
        """Deve formatar como percentual."""
        assert formatar_percentual(85.5) == "85.5%"

    def test_formatar_percentual_casas_decimais(self):
        """Deve respeitar casas decimais."""
        assert formatar_percentual(85.567, 2) == "85.57%"

    def test_formatar_numero(self):
        """Deve formatar com separador de milhar."""
        assert formatar_numero(1000000) == "1.000.000"


# =============================================================================
# TESTES DE CÁLCULOS DE NEGÓCIO
# =============================================================================

class TestCalculosNegocio:
    """Testes para funções de cálculo."""

    def test_calcular_taxa_ocupacao(self):
        """Deve calcular taxa de ocupação corretamente."""
        assert calcular_taxa_ocupacao(80, 100) == 80.0

    def test_calcular_taxa_ocupacao_zero_leitos(self):
        """Deve retornar 0 se total de leitos é zero."""
        assert calcular_taxa_ocupacao(50, 0) == 0.0

    def test_calcular_tempo_medio_espera(self):
        """Deve calcular média corretamente."""
        valores = [2, 4, 6, 8]
        assert calcular_tempo_medio_espera(valores) == 5.0

    def test_calcular_tempo_medio_espera_vazio(self):
        """Deve retornar 0 para lista vazia."""
        assert calcular_tempo_medio_espera([]) == 0.0

    def test_calcular_giro_leitos(self):
        """Deve calcular giro de leitos."""
        assert calcular_giro_leitos(500, 100) == 5.0

    def test_calcular_giro_leitos_zero(self):
        """Deve retornar 0 se leitos é zero."""
        assert calcular_giro_leitos(100, 0) == 0.0

    def test_calcular_variacao(self):
        """Deve calcular variação percentual."""
        assert calcular_variacao(120, 100) == 20.0

    def test_calcular_variacao_reducao(self):
        """Deve calcular variação negativa."""
        assert calcular_variacao(80, 100) == -20.0

    def test_calcular_variacao_zero_anterior(self):
        """Deve retornar 0 se valor anterior é zero."""
        assert calcular_variacao(100, 0) == 0.0


# =============================================================================
# TESTES DE CLASSIFICAÇÃO
# =============================================================================

class TestClassificacao:
    """Testes para funções de classificação."""

    def test_classificar_ocupacao_baixa(self):
        """Deve classificar como baixa."""
        resultado = classificar_ocupacao(60)
        assert resultado["classificacao"] == "Baixa"
        assert resultado["icone"] == "🟢"

    def test_classificar_ocupacao_normal(self):
        """Deve classificar como normal."""
        resultado = classificar_ocupacao(75)
        assert resultado["classificacao"] == "Normal"

    def test_classificar_ocupacao_atencao(self):
        """Deve classificar como atenção."""
        resultado = classificar_ocupacao(87)
        assert resultado["classificacao"] == "Atenção"
        assert resultado["cor"] == "#ffa502"

    def test_classificar_ocupacao_critica(self):
        """Deve classificar como crítica."""
        resultado = classificar_ocupacao(92)
        assert resultado["classificacao"] == "Crítica"

    def test_classificar_ocupacao_colapso(self):
        """Deve classificar como colapso."""
        resultado = classificar_ocupacao(97)
        assert resultado["classificacao"] == "Colapso"
        assert resultado["icone"] == "🔴"

    def test_classificar_tempo_espera_excelente(self):
        """Deve classificar como excelente."""
        resultado = classificar_tempo_espera(1.5)
        assert resultado["classificacao"] == "Excelente"

    def test_classificar_tempo_espera_critico(self):
        """Deve classificar como crítico."""
        resultado = classificar_tempo_espera(10)
        assert resultado["classificacao"] == "Crítico"


# =============================================================================
# TESTES DE GERADOR DE DADOS
# =============================================================================

class TestGeradorDados:
    """Testes para geração de dados sintéticos."""

    def test_gerar_dados_colunas(self):
        """Deve gerar DataFrame com colunas esperadas."""
        df = gerar_dados_sinteticos(num_dias=10)
        assert 'Data' in df.columns
        assert 'Ocupacao' in df.columns
        assert 'Leitos_Disponiveis' in df.columns

    def test_gerar_dados_linhas(self):
        """Deve gerar número correto de linhas."""
        df = gerar_dados_sinteticos(num_dias=30)
        assert len(df) == 30

    def test_gerar_dados_reproducibilidade(self):
        """Deve ser reproduzível com mesma seed."""
        df1 = gerar_dados_sinteticos(num_dias=30, seed=42)
        df2 = gerar_dados_sinteticos(num_dias=30, seed=42)
        assert df1['Ocupacao'].equals(df2['Ocupacao'])

    def test_gerar_dados_faixa_ocupacao(self):
        """Ocupação deve estar na faixa válida."""
        df = gerar_dados_sinteticos(num_dias=100)
        assert df['Ocupacao'].min() >= 50
        assert df['Ocupacao'].max() <= 98


# =============================================================================
# TESTES DE CASOS EXTREMOS (EDGE CASES)
# =============================================================================

class TestEdgeCases:
    """Testes para casos extremos."""

    def test_ocupacao_valor_negativo(self):
        """Deve lidar com valores negativos."""
        # A função deve aceitar, mas classificação lida com isso
        resultado = classificar_ocupacao(-10)
        # Valor negativo classifica como baixa
        assert resultado["classificacao"] == "Baixa"

    def test_ocupacao_acima_100(self):
        """Deve classificar acima de 100 como colapso."""
        resultado = classificar_ocupacao(110)
        assert resultado["classificacao"] == "Colapso"

    def test_tempo_espera_zero(self):
        """Deve classificar tempo zero como excelente."""
        resultado = classificar_tempo_espera(0)
        assert resultado["classificacao"] == "Excelente"

    def test_formatar_valor_negativo(self):
        """Deve formatar valores negativos."""
        resultado = formatar_moeda(-1000.50)
        assert "-1,000.50" in resultado