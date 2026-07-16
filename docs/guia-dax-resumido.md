# 📊 Dashboard Hospitalar - Guia de Medidas DAX

## KPIs Principais

### 1. Taxa de Ocupação de Leitos

```dax
Taxa Ocupação = 
DIVIDE(
    [Leitos Ocupados],
    [Total Leitos Disponíveis],
    0
)
```

**Meta**: 75-85%
**Interpretação**: Valores acima de 90% indicam sobrecarga.

---

### 2. Tempo Médio de Espera

```dax
Tempo Médio Espera (Horas) = 
AVERAGE(F_Internacoes[Tempo_Espera_Horas])
```

**Meta**: < 4 horas
**Interpretação**: Valores elevados indicam gargalo na admissão.

---

### 3. Custo por Paciente

```dax
Custo Médio por Paciente = 
DIVIDE(
    SUM(F_Internacoes[Custo_Procedimento]),
    DISTINCTCOUNT(F_Internacoes[Id_Paciente]),
    0
)
```

**Interpretação**: Acompanhar evolução mensal e comparar por especialidade.

---

### 4. Taxa de Readmissão (30 dias)

```dax
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

**Meta**: < 10%
**Interpretação**: Valores elevados podem indicar qualidade assistencial deficiente.

---

## Medidas de Tempo

### Dias de Internação

```dax
Dias Internação = 
AVERAGEX(
    F_Internacoes,
    DATEDIFF(
        F_Internacoes[Data_Entrada],
        COALESCE(F_Internacoes[Data_Alta], TODAY()),
        DAY
    )
)
```

---

## Medidas YTD/MTD

```dax
Custo YTD = TOTALYTD([Custo Total], D_Tempo[Data])
Custo MTD = CALCULATE([Custo Total], DATESMTD(D_Tempo[Data]))
```

---

## Medidas de Comparação

```dax
Variação vs. Mês Anterior = 
VAR CustoAtual = [Custo Total]
VAR CustoMesAnterior = CALCULATE([Custo Total], PREVIOUSMONTH(D_Tempo[Data]))
RETURN DIVIDE(CustoAtual - CustoMesAnterior, CustoMesAnterior, 0)
```

---

## Dicas de Performance

1. **Evite CALCULATE aninhados** sempre que possível
2. **Use variáveis** para melhorar legibilidade e performance
3. **Prefira SUMX/FILTER** a múltiplos CALCULATE
4. **Documente medidas complexas** com comentários

---

Para a lista completa de medidas, consulte `docs/medidas-dax.md`.