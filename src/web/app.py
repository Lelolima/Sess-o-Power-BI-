"""
Dashboard Hospitalar - Versão Web (Streamlit)

Dashboard interativo de análise de dados hospitalares para portfólio de BI.
Simula KPIs reais de gestão hospitalar com visualizações em Plotly.

Autor: Wellington de Lima Catarina
Data: 2026-07-15
"""

from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from typing import Tuple, Dict

try:
    from src.web.utils import calcular_giro_leitos
except ImportError:  # execução via `streamlit run src/web/app.py`
    from utils import calcular_giro_leitos

# ============================================================================
# CONFIGURAÇÕES GLOBAIS
# ============================================================================

# Constantes de negócio (evitar magic numbers)
META_OCUPACAO = 80.0  # Percentual
ALERTA_OCUPACAO = 90.0  # Percentual
RANDOM_SEED = 42
NUM_DIAS = 365
DATA_INICIO = '2024-01-01'

# Paleta de cores
CORES = {
    'primaria': '#00d9ff',
    'alerta': '#ffa502',
    'critico': '#ff6b6b',
    'sucesso': '#2d8a2d',
    'background': '#1a1a2e',
}

ESPECIALIDADES = [
    'Cardiologia', 'Ortopedia', 'Neurologia', 'Pediatria',
    'Oncologia', 'Gastroenterologia', 'Pneumologia', 'Nefrologia'
]

MESES = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Configurações da página
st.set_page_config(
    page_title="Dashboard Hospitalar",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown(f"""
<style>
    .metric-card {{
        background-color: {CORES['background']};
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }}
    .metric-value {{
        font-size: 2.5rem;
        font-weight: bold;
        color: {CORES['primaria']};
    }}
    .metric-label {{
        font-size: 0.9rem;
        color: #888;
    }}
    .stAlert {{
        margin-bottom: 1rem;
    }}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# FUNÇÕES DE CARREGAMENTO DE DADOS
# ============================================================================

@st.cache_data
def carregar_dados() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carrega dados sintéticos para demonstração do dashboard.

    Em produção, estes dados viriam de:
    - Banco de dados SQL
    - API REST
    - Arquivos CSV/Parquet

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]:
            - DataFrame de ocupação diária
            - DataFrame de custos por especialidade
    """
    try:
        np.random.seed(RANDOM_SEED)

        # Datas
        datas = pd.date_range(DATA_INICIO, periods=NUM_DIAS, freq='D')

        # Dados de ocupação com sazonalidade realista
        base_ocupacao = 82 + 5 * np.sin(np.arange(NUM_DIAS) * 2 * np.pi / 365)
        ocupacao = pd.DataFrame({
            'Data': datas,
            'Ocupacao': np.clip(base_ocupacao + np.random.normal(0, 5, NUM_DIAS), 50, 98),
            'Leitos_Disponiveis': np.random.randint(180, 220, NUM_DIAS),
        })

        # Dados por especialidade com distribuição realista
        n_registros = len(ESPECIALIDADES) * 12
        dados_especialidade = pd.DataFrame({
            'Especialidade': ESPECIALIDADES * 12,
            'Mes': MESES * len(ESPECIALIDADES),
            'Custo_Medio': np.random.uniform(3000, 8000, n_registros),
            'Pacientes': np.random.randint(50, 200, n_registros),
            'Tempo_Espera': np.random.uniform(1, 24, n_registros),
        })

        return ocupacao, dados_especialidade

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame(), pd.DataFrame()


# ============================================================================
# FUNÇÕES DE VISUALIZAÇÃO
# ============================================================================

def calcular_kpis_operacionais(ocupacao_df: pd.DataFrame, dados_esp: pd.DataFrame) -> Dict[str, float]:
    """Calcula giro de leitos e tempo médio de espera a partir dos dados carregados.

    Antes estes KPIs eram sorteados com np.random a cada renderização,
    sem relação com os dados exibidos.
    """
    leitos_medios = float(ocupacao_df['Leitos_Disponiveis'].mean())
    ultimo_mes = dados_esp[dados_esp['Mes'] == MESES[-1]]
    penultimo_mes = dados_esp[dados_esp['Mes'] == MESES[-2]]
    giro = calcular_giro_leitos(int(ultimo_mes['Pacientes'].sum()), leitos_medios)
    giro_anterior = calcular_giro_leitos(int(penultimo_mes['Pacientes'].sum()), leitos_medios)
    return {
        'giro_leitos': giro,
        'delta_giro': giro - giro_anterior,
        'tempo_espera': float(ultimo_mes['Tempo_Espera'].mean()),
        'tempo_espera_medio': float(dados_esp['Tempo_Espera'].mean()),
    }


def criar_cards_kpis(ocupacao_df: pd.DataFrame, dados_esp: pd.DataFrame) -> None:
    """Cria cards com KPIs principais"""

    col1, col2, col3, col4 = st.columns(4)

    ocupacao_media = ocupacao_df['Ocupacao'].mean()
    leitos_medios = ocupacao_df['Leitos_Disponiveis'].mean()
    dia_atual = ocupacao_df.iloc[-1]
    kpis = calcular_kpis_operacionais(ocupacao_df, dados_esp)

    with col1:
        st.metric(
            label="🏥 Taxa de Ocupação",
            value=f"{dia_atual['Ocupacao']:.1f}%",
            delta=f"{dia_atual['Ocupacao'] - ocupacao_media:.1f}%"
        )

    with col2:
        st.metric(
            label="🛏️ Leitos Disponíveis",
            value=f"{dia_atual['Leitos_Disponiveis']:.0f}",
            delta=f"{dia_atual['Leitos_Disponiveis'] - leitos_medios:.0f}"
        )

    with col3:
        st.metric(
            label="🔄 Giro de Leitos (mês)",
            value=f"{kpis['giro_leitos']:.1f}",
            delta=f"{kpis['delta_giro']:+.1f}"
        )

    with col4:
        st.metric(
            label="⏱️ Tempo Médio Espera",
            value=f"{kpis['tempo_espera']:.1f}h",
            delta=f"{kpis['tempo_espera'] - kpis['tempo_espera_medio']:.1f}h",
            delta_color="inverse"
        )


def criar_grafico_ocupacao(ocupacao_df):
    """Cria gráfico de linha da ocupação"""

    fig = go.Figure()

    # Linha principal
    fig.add_trace(go.Scatter(
        x=ocupacao_df['Data'],
        y=ocupacao_df['Ocupacao'],
        mode='lines',
        name='Ocupação (%)',
        line=dict(color='#00d9ff', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 217, 255, 0.1)'
    ))

    # Linha de meta
    fig.add_hline(
        y=80,
        line_dash="dash",
        line_color="#ff6b6b",
        annotation_text="Meta: 80%",
        annotation_position="top right"
    )

    # Linha de alerta
    fig.add_hline(
        y=90,
        line_dash="dash",
        line_color="#ffa502",
        annotation_text="Alerta: 90%",
        annotation_position="top right"
    )

    fig.update_layout(
        title='📈 Evolução da Ocupação de Leitos',
        xaxis_title='Data',
        yaxis_title='Ocupação (%)',
        template='plotly_dark',
        height=400,
        showlegend=True,
        hovermode='x unified'
    )

    return fig


def criar_heatmap_especialidades(dados_esp):
    """Cria heatmap por especialidade"""

    # Pivotar dados para heatmap
    pivot = dados_esp.pivot_table(
        values='Custo_Medio',
        index='Especialidade',
        columns='Mes',
        aggfunc='mean'
    )

    fig = px.imshow(
        pivot,
        color_continuous_scale='RdYlBu_r',
        title='💰 Custo Médio por Especialidade (Heatmap)',
        labels={'x': 'Mês', 'y': 'Especialidade', 'color': 'Custo (R$)'}
    )

    fig.update_layout(
        template='plotly_dark',
        height=500,
        font=dict(size=10)
    )

    return fig


def criar_grafico_especialidades(dados_esp):
    """Cria gráfico de barras por especialidade"""

    # Agrupar por especialidade
    resumo = dados_esp.groupby('Especialidade').agg({
        'Custo_Medio': 'mean',
        'Pacientes': 'sum',
        'Tempo_Espera': 'mean'
    }).reset_index()

    # Gráfico de custo
    fig_custo = px.bar(
        resumo.sort_values('Custo_Medio', ascending=False),
        x='Especialidade',
        y='Custo_Medio',
        color='Custo_Medio',
        color_continuous_scale='Reds',
        title='💰 Custo Médio por Especialidade',
        template='plotly_dark'
    )

    fig_custo.update_layout(
        height=400,
        showlegend=False,
        xaxis_title='Especialidade',
        yaxis_title='Custo Médio (R$)'
    )

    return fig_custo


def main():
    """Função principal do dashboard"""

    # Sidebar
    st.sidebar.image(
        "https://img.shields.io/badge/Power%20BI-Desktop-F2C811?logo=powerbi",
        use_container_width=True
    )

    st.sidebar.markdown("""
    ### 🏥 Dashboard Hospitalar

    Sistema de Business Intelligence
    para análise de dados hospitalares.

    **Desenvolvido por:** Wellington de Lima Catarina

    [LinkedIn](https://www.linkedin.com/in/wellington-de-lima-catarina/) |
    [GitHub](https://github.com/Lelolima)
    """)

    # Menu de páginas
    pagina = st.sidebar.radio(
        "📊 Navegação",
        ["Visão Geral", "Análise por Especialidade", "Custos e Faturamento", "Sobre"]
    )

    # Carregar dados
    ocupacao_df, dados_esp = carregar_dados()
    st.sidebar.info("Dados sintéticos gerados para demonstração; não são dados hospitalares reais.")

    if pagina == "Visão Geral":
        st.title("🏥 Dashboard de Análise Hospitalar")

        st.markdown("""
        Este dashboard apresenta os principais KPIs de gestão hospitalar,
        permitindo monitorar ocupação de leitos, custos e eficiência operacional.
        """)

        # Cards KPI
        criar_cards_kpis(ocupacao_df, dados_esp)

        st.divider()

        # Gráficos
        col1, col2 = st.columns(2)

        with col1:
            fig_ocupacao = criar_grafico_ocupacao(ocupacao_df)
            st.plotly_chart(fig_ocupacao, use_container_width=True)

        with col2:
            # Gauge chart de ocupação
            ocupacao_atual = ocupacao_df['Ocupacao'].iloc[-1]

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=ocupacao_atual,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Ocupação Atual", 'font': {'size': 24}},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#00d9ff"},
                    'steps': [
                        {'range': [0, 80], 'color': '#1e3a1e'},
                        {'range': [80, 90], 'color': '#3a3a1e'},
                        {'range': [90, 100], 'color': '#3a1e1e'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))

            fig_gauge.update_layout(height=400)
            st.plotly_chart(fig_gauge, use_container_width=True)

    elif pagina == "Análise por Especialidade":
        st.title("📊 Análise por Especialidade")

        col1, col2 = st.columns(2)

        with col1:
            fig_especialidades = criar_grafico_especialidades(dados_esp)
            st.plotly_chart(fig_especialidades, use_container_width=True)

        with col2:
            # Dados de tempo de espera
            tempo_by_esp = dados_esp.groupby('Especialidade')['Tempo_Espera'].mean().reset_index()

            fig_tempo = px.bar(
                tempo_by_esp.sort_values('Tempo_Espera', ascending=False),
                x='Especialidade',
                y='Tempo_Espera',
                color='Tempo_Espera',
                color_continuous_scale='Oranges',
                title='⏱️ Tempo Médio de Espera por Especialidade',
                template='plotly_dark'
            )

            st.plotly_chart(fig_tempo, use_container_width=True)

        st.divider()
        st.subheader("📋 Dados Detalhados")
        st.dataframe(dados_esp.head(50), use_container_width=True)

    elif pagina == "Custos e Faturamento":
        st.title("💰 Custos e Faturamento")

        fig_heatmap = criar_heatmap_especialidades(dados_esp)
        st.plotly_chart(fig_heatmap, use_container_width=True)

        st.divider()

        # Estatísticas
        col1, col2, col3 = st.columns(3)

        custo_total = dados_esp['Custo_Medio'].sum()
        custo_medio = dados_esp['Custo_Medio'].mean()
        total_pacientes = dados_esp['Pacientes'].sum()

        col1.metric("Custo Total (Demo)", f"R$ {custo_total:,.2f}")
        col2.metric("Custo Médio", f"R$ {custo_medio:,.2f}")
        col3.metric("Pacientes Atendidos", f"{total_pacientes:,.0f}")

    elif pagina == "Sobre":
        st.title("ℹ️ Sobre o Projeto")

        st.markdown("""
        ### 🏥 Dashboard Hospitalar Power BI

        Este projeto é um portfólio de Business Intelligence focado em **Healthcare Analytics**,
        demonstrando as melhores práticas de desenvolvimento de dashboards no Power BI.

        **Tecnologias Utilizadas:**
        - 📊 Power BI Desktop
        - 🐍 Python (Pandas, Streamlit, Plotly)
        - 📈 DAX para medidas e cálculos
        - 🗄️ SQL Server para modelagem de dados

        ### 👤 Autor

        **Wellington de Lima Catarina**
        - Business Intelligence Developer
        - Especialista em Healthcare Analytics

        🔗 **Conexões:**
        - [LinkedIn](https://www.linkedin.com/in/wellington-de-lima-catarina/)
        - [GitHub](https://github.com/Lelolima)
        - Email: lelolima806@gmail.com

        ### 📄 Licença

        Este projeto está licenciado sob a [MIT License](https://github.com/Lelolima/portfolio-bi-wellington-lima/blob/main/LICENSE)
        """)


if __name__ == "__main__":
    main()