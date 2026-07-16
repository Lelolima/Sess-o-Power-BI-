# Estudo de Caso: Análise Hospitalar

## Contexto

Este estudo de caso apresenta o desenvolvimento de um dashboard de Business Intelligence para gestão hospitalar, focado em otimização de recursos e redução de custos operacionais.

## Problema de Negócio

### Cenário Atual

Um hospital de médio porte (200 leitos, 500+ funcionários) enfrentava os seguintes desafios:

1. **Gestão de Leitos**
   - Dificuldade em monitorar ocupação em tempo real
   - Tempo de espera elevado para UTI
   - Distribuição inadequada por especialidade

2. **Análise de Custos**
   - Falta de visibilidade sobre custos por procedimento
   - Rateios complexos entre departamentos
   - Orçamento vs. Real apenas mensal

3. **Qualidade Assistencial**
   - Readmissões não monitoradas sistematicamente
   - Tempo de espera não rastreado
   - Variações de prática entre médicos

## Solução Implementada

### Dashboard Power BI

**Página 1: Visão Geral**
- Cards com KPIs principais
- Gráfico de tendência de ocupação
- Mapa de calor por especialidade

**Página 2: Analítico de Leitos**
- Waterfall de entradas/saídas
- Gauge de ocupação por unidade
- Decomposition tree de variâncias

**Página 3: Custos e Faturamento**
- Custo por procedimento (boxplot)
- Orçamento vs. Real (accumulated)
- Top 10 procedimentos por custo

**Página 4: Qualidade e Readmissão**
- Taxa de readmissão porspecialidade
- Tempo médio de espera (trend)
- Análise de variância por médico

### Medidas DAX Desenvolvidas

```dax
-- Leitos Ocupados (snapshot diário)
Leitos Ocupados = 
CALCULATE(
    COUNTROWS(F_Internacoes),
    F_Internacoes[Data_Entretrica] <= MAX(D_Tempo[Data]),
    F_Internacoes[Data_Alta] >= MAX(D_Tempo[Data])
        || ISBLANK(F_Internacoes[Data_Alta])
)

-- Readmissão em 30 dias
Readmissões 30 dias = 
VAR PacientesAlta = 
    CALCULATETABLE(
        VALUES(F_Internacoes[Id_Paciente]),
        F_Internacoes[Data_Alta] <= MAX(D_Tempo[Data]) - 30
    )
RETURN
CALCULATE(
    COUNTROWS(F_Internacoes),
    F_Internacoes[Id_Paciente] IN PacientesAlta,
    F_Internacoes[Data_Entretrica] <= MAX(D_Tempo[Data])
)

-- Tempo Médio de Espera (horas)
Tempo Médio Espera = 
AVERAGE(F_Internacoes[Tempo_Espera_Horas])
```

## Resultados Alcançados

### Métricas de Impacto

| Indicador | Antes | Depois | Variação |
|-----------|-------|--------|----------|
| Tempo de análise de reports | 4 horas/dia | 30 min/dia | -87% |
| Ocupação média UTI | 92% | 84% | -8 pp |
| Tempo médio espera (emergenca) | 6.2h | 3.8h | -39% |
| Readmissão (cirurgia cardíaca) | 14% | 9% | -35% |

### Economia Financeira Estimada

- **Redução de custos operacionais**: R$ 180.000/ano
- ** tránh de readmissões**: R$ 420.000/ano
- **Ganho de eficiência (equipe)**: R$ 96.000/ano

**Total estimado**: R$ 696.000/ano

## Lições Aprendidas

### O que Funcionou

1. **Envolvimento dos Stakeholders**
   - Reuniões semanais com gestores
   - Validação iterativa de visualizações

2. **Foco em Ação**
   - Cada KPI com responsável definido
   - Metas claras e acompanhadas

3. **Design Centrado no Usuário**
   - Navegação intuitiva
   - Cores semânticas (verde/bom, vermelho/atenção)

### Desafios Superados

1. **Qualidade dos Dados**
   - Implementação de validações no ETL
   - Feedback automático de inconsistências

2. **Adoção da Equipe**
   - Treinamentos presenciais
   - Material de apoio em PDF

3. **Performance**
   - Otimização de medidas DAX
   - Incremental refresh

## Próximos Passos

1. **Integração com Teams**: Alertas automáticos de ocupação crítica
2. **Mobile**: Versão responsiva para tablets
3. **Predição**: Modelo ML para previsão de demanda
4. **API**: Integração contínua com ERP

---

## Sobre o Autor

**Wellington de Lima Catarina**
- Business Intelligence Developer
- Especialista em Healthcare Analytics
- LinkedIn: [linkedin.com/in/wellington-de-lima-catarina](https://www.linkedin.com/in/wellington-de-lima-catarina/)