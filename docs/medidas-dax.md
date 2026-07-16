# Medidas DAX - Dashboard Hospitalar

## Tabela de Medidas

### KPIs Principais

#### 1. Taxa de Ocupação de Leitos

```dax
Taxa Ocupação = 
DIVIDE(
    [Leitos Ocupados],
    [Total Leitos Disponíveis],
    0
)

Leitos Ocupados = 
CALCULATE(
    COUNTROWS(F_Internacoes),
    F_Internacoes[Data_Entretrica] <= MAX(D_Tempo[Data]),
    F_Internacoes[Data_Alta] >= MAX(D_Tempo[Data])
        || ISBLANK(F_Internacoes[Data_Alta])
)

Total Leitos Disponíveis = 
MAX(D_Leitos[Quantidade_Leitos])
```

#### 2. Tempo Médio de Espera

```dax
Tempo Médio Espera (Horas) = 
AVERAGE(F_Internacoes[Tempo_Espera_Horas])

Tempo Médio Espera (Dias) = 
DIVIDE(
    [Tempo Médio Espera (Horas)],
    24,
    0
)
```

#### 3. Custo por Procedimento

```dax
Custo Total = 
SUM(F_Internacoes[Custo_Procedimento])

Custo Médio por Paciente = 
DIVIDE(
    [Custo Total],
    DISTINCTCOUNT(F_Internacoes[Id_Paciente]),
    0
)

Custo por Leito-Dia = 
DIVIDE(
    [Custo Total],
    SUM(F_Internacoes[Dias_Internacao],
    0
)
```

#### 4. Taxa de Readmissão

```dax
Taxa Readmissão 30 dias = 
VAR TotalAltas = 
    CALCULATE(
        COUNTROWS(F_Internacoes),
        NOT(ISBLANK(F_Internacoes[Data_Alta]))
    )
VAR Readmissoes = 
    CALCULATE(
        COUNTROWS(F_Internacoes),
        F_Internacoes[Readmissao_Flag] = 1
    )
RETURN
DIVIDE(
    Readmissoes,
    TotalAltas,
    0
)

-- Flag de readmissão (precedimento calculado)
Readmissao Flag = 
VAR DataAltaAtual = MAX(F_Internacoes[Data_Alta])
VAR IdPaciente = MAX(F_Internacoes[Id_Paciente])
VAR ProximaInternacao = 
    CALCULATE(
        MIN(F_Internacoes[Data_Entretrica]),
        ALLEXCEPT(F_Internacoes, F_Internacoes[Id_Paciente]),
        F_Internacoes[Data_Entretrica] > DataAltaAtual
    )
RETURN
IF(
    DATEDIFF(DataAltaAtual, ProximaInternacao, DAY) <= 30,
    1,
    0
)
```

### Medidas de Tempo

#### 5. Dias de Internação

```dax
Dias Internação = 
AVERAGEX(
    F_Internacoes,
    DATEDIFF(
        F_Internacoes[Data_Entretrica],
        COALESCE(F_Internacoes[Data_Alta], TODAY()),
        DAY
    )
)

Dias Internação Total = 
SUMX(
    F_Internacoes,
    DATEDIFF(
        F_Internacoes[Data_Entretrica],
        COALESCE(F_Internacoes[Data_Alta], TODAY()),
        DAY
    )
)
```

#### 6. Giro de Leitos

```dax
Giro de Leitos = 
DIVIDE(
    COUNTROWS(F_Internacoes),
    [Total Leitos Disponíveis],
    0
)
```

### Medidas YTD/MTD

```dax
Custo YTD = 
TOTALYTD(
    [Custo Total],
    D_Tempo[Data]
)

Internações MTD = 
CALCULATE(
    COUNTROWS(F_Internacoes),
    DATESMTD(D_Tempo[Data])
)

Custo MTD = 
CALCULATE(
    [Custo Total],
    DATESMTD(D_Tempo[Data])
)
```

### Medidas de Comparação

```dax
Variação vs. Mês Anterior = 
VAR CustoAtual = [Custo Total]
VAR CustoMesAnterior = 
    CALCULATE(
        [Custo Total],
        PREVIOUSMONTH(D_Tempo[Data])
    )
RETURN
DIVIDE(
    CustoAtual - CustoMesAnterior,
    CustoMesAnterior,
    0
)

Variação vs. Mesmo Período Ano Anterior = 
VAR CustoAtual = [Custo Total]
VAR CustoAnoAnterior = 
    CALCULATE(
        [Custo Total],
        SAMEPERIODLASTYEAR(D_Tempo[Data])
    )
RETURN
DIVIDE(
    CustoAtual - CustoAnoAnterior,
    CustoAnoAnterior,
    0
)
```

## Medidas de Segmentação

### por Especialidade

```dax
Custo por Especialidade = 
CALCULATE(
    [Custo Total],
    ALLEXCEPT(F_Internacoes, D_Procedimentos[Especialidade])
)

Ranking Especialidade = 
RANKX(
    ALL(D_Procedimentos[Especialidade]),
    [Custo por Especialidade],
    ,
    DESC,
    DENSE
)
```

### por Médico

```dax
Custo por Médico = 
CALCULATE(
    [Custo Total],
    ALLEXCEPT(F_Internacoes, D_Medicos)
)

Tempo Médio por Médico = 
CALCULATE(
    [Tempo Médio Espera (Horas)],
    ALLEXCEPT(F_Internacoes, D_Medicos)
)
```

## Medidas de Metas

```dax
Meta Ocupação = 0.80  -- 80%

Status Meta Ocupação = 
VAR Atual = [Taxa Ocupação]
VAR Meta = [Meta Ocupação]
RETURN
SWITCH(
    TRUE(),
    Atual <= Meta * 0.9, "🟢 Abaixo",
    Atual <= Meta, "🟡 Perto",
    Atual <= Meta * 1.1, "🟠 Acima",
    "🔴 Crítico"
)

Desvio da Meta = 
[Taxa Ocupação] - [Meta Ocupação]
```