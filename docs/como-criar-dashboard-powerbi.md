# Instruções para Criar o Dashboard Power BI

## Passo 1: Importar Dados

1. Abra o **Power BI Desktop**
2. Clique em **Obter Dados** > **Texto/CSV**
3. Importe os arquivos da pasta `data/`:
   - `pacientes_sample.csv`
   - `internacoes_sample.csv`
   - `medicos_sample.csv`
   - `leitos_sample.csv`
4. Clique em **Carregar**

## Passo 2: Criar Relacionamentos

Vá para a visão de **Modelo** e crie:

```
D_Pacientes[Id_Paciente] ── F_Internacoes[Id_Paciente] (1 para Muitos)
D_Medicos[Id_Medico] ───── F_Internacoes[Id_Medico] (1 para Muitos)
D_Leitos[Id_Leito] ─────── F_Internacoes[Leito] (1 para Muitos)
```

## Passo 3: Criar Tabela Calendário

Em **Modelagem** > **Nova Tabela**:

```dax
D_Tempo = 
ADDCOLUMNS(
    CALENDAR(DATE(2024,1,1), DATE(2026,12,31)),
    "Ano", YEAR([Date]),
    "Mes", FORMAT([Date], "MMM"),
    "NumeroMes", MONTH([Date]),
    "Trimestre", "T" & FORMAT([Date], "Q"),
    "DiaSemana", FORMAT([Date], "ddd")
)
```

Relacione com `F_Internacoes[Data_Entrada]`.

## Passo 4: Criar Medidas

Copie as medidas de `docs/medidas-dax.md` e crie no Power BI:

```dax
Taxa Ocupação = DIVIDE([Leitos Ocupados], [Total Leitos Disponíveis], 0)
Tempo Médio Espera = AVERAGE(F_Internacoes[Tempo_Espera_Horas])
Custo Total = SUM(F_Internacoes[Custo_Procedimento])
```

## Passo 5: Criar Páginas

### Página 1: Visão Geral
- Cards com KPIs principais
- Gráfico de linha (ocupação)
- Gauge chart (meta de ocupação)

### Página 2: Análise por Especialidade
- Barras por especialidade
- Heatmap de custos
- Tabela detalhada

### Página 3: Custos e Faturamento
- Custo por procedimento
- Orçamento vs. Real
- Top 10 procedimentos

### Página 4: Qualidade e Readmissão
- Taxa de readmissão
- Tempo de espera
- Análise por médico

## Passo 6: Formatação

1. Tema: **Escuro** (Dark)
2. Cores principais:
   - Primária: `#00d9ff` (ciano)
   - Alerta: `#ffa502` (laranja)
   - Crítico: `#ff6b6b` (vermelho)
3. Fonte: **Segoe UI**

## Passo 7: Salvar e Exportar

1. Salve como `dashboards/Dashboard-Hospitalar.pbix`
2. Exporte PDF para `dashboards/Dashboard-Hospitalar.pdf`
3. Capture screenshots para `screenshots/`

---

## Dicas de Design

- Use **espaçamento consistente** (8px grid)
- Alinhe todos os visuais
- Use **tooltips** customizados
- Adicione **ícones** para cada KPI
- Mantenha **hierarquia visual** clara

---

Verifique `docs/powerbi-referencia.md` para mais detalhes.