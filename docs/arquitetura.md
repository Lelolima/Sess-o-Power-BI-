# Arquitetura do Dashboard Hospitalar

## Visão Geral

Este documento descreve a arquitetura completa da solução de Business Intelligence para análise hospitalar.

## Componentes

### 1. Camada de Dados (Data Sources)

```
┌─────────────────────────────────────────────────────────────┐
│                    FONTES DE DADOS                          │
├─────────────────┬─────────────────┬─────────────────────────┤
│   ERP Hospital  │   Planilhas     │   Banco de Dados        │
│   (TASY/RMV)    │   Excel         │   SQL Server            │
├─────────────────┼─────────────────┼─────────────────────────┤
│ - Pacientes     │ - Metas         │ - Histórico de          │
│ - Internações   │ - Orçamento     │   consultas             │
│ - Procedimentos │ - Rateios       │ - Cadastro de médicos   │
│ - Faturamento   │                 │ - Leitos/Especialidades │
└─────────────────┴─────────────────┴─────────────────────────┘
```

### 2. Camada de ETL

**Power Query (M)**:
- Conexão direta com fontes
- Limpeza e padronização
- Mesclagem de tabelas
- Cálculos preliminares

**Python (Pandas)**:
- Scripts de ETL avançados
- Validação de qualidade
- Anonimização de dados sensíveis

### 3. Modelagem de Dados

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   D_Pacientes│────▶│ F_Internacoes│◀────│ D_Tempo      │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ▼
                   ┌──────────────┐
                   │  D_Procedimentos│
                   └──────────────┘
```

**Tabela Fact**: `F_Internacoes`
- Chaves estrangeiras para todas as dimensões
- Métricas: dias_internacao, custo, readmissao_flag

**Tabelas Dimensão**:
- `D_Pacientes`: id, idade, sexo, regiao
- `D_Tempo`: data, mes, ano, trimestre
- `D_Procedimentos`: id, nome, especialidade, complexo

### 4. Camada de Visualização

**Power BI Desktop**:
- 4 páginas principais
- 15+ visualizações
- 20+ medidas DAX

**Streamlit (Web)**:
- Versão alternativa em Python
- Deploy no Netlify/Render

## Medidas DAX Principais

```dax
-- Taxa de Ocupação de Leitos
Taxa Ocupação = 
DIVIDE(
    [Leitos Ocupados],
    [Total Leitos Disponíveis],
    0
)

-- Tempo Médio de Espera
Tempo Médio Espera = 
AVERAGE(F_Internacoes[Tempo_Espera_Horas])

-- Custo por Procedimento
Custo Total = 
SUM(F_Internacoes[Custo_Procedimento])

-- Taxa de Readmissão (30 dias)
Taxa Readmissão = 
DIVIDE(
    CALCULATE(
        COUNTROWS(F_Internacoes),
        F_Internacoes[Readmissao_Flag] = 1
    ),
    COUNTROWS(F_Internacoes),
    0
)
```

## KPIs Monitorados

| KPI | Fórmula | Meta |
|-----|---------|------|
| Taxa de Ocupação | Leitos Ocupados / Total Leitos | 75-85% |
| Tempo Médio Espera | média(horas) | < 4h |
| Custo por Paciente | Σ Custos / N Pacientes | - |
| Taxa de Readmissão | Readmissões / Total Altas | < 10% |

## Segurança

- Dados anonimizados em ambientes de desenvolvimento
- Row-Level Security (RLS) para usuários por região
- Logs de acesso e auditoria

## Performance

- Incremental refresh para dados históricos
- Aggregations para grandes volumes
- DirectQuery apenas para dados em tempo real