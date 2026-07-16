# 📊 Power BI - Guia de Referência Rápida

## Conexão com Dados

### Importando CSV

1. No Power BI Desktop, clique em `Obter Dados` > `Texto/CSV`
2. Navegue até a pasta `data/` no projeto
3. Selecione o arquivo desejado
4. Clique em `Carregar`

### Transformar Dados (Power Query)

1. Clique em `Transformar Dados` para abrir o Power Query Editor
2. Aplique transformações:
   - Tipos de dados (texto, número, data)
   - Colunas personalizadas
   - Mesclagem de consultas
3. Clique em `Fechar e Aplicar`

---

## Modelagem de Dados

### Relacionamentos

```
F_Internacoes (1) ── (*) D_Pacientes
F_Internacoes (1) ── (*) D_Tempo
F_Internacoes (1) ── (*) D_Procedimentos
F_Internacoes (1) ── (*) D_Medicos
F_Internacoes (1) ── (*) D_Leitos
```

### Tabela Calendário (D_Tempo)

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

---

## Visualizações Recomendadas

| KPI | Visual Recomendado |
|-----|-------------------|
| Ocupação atual | Cartão (Card) |
| Evolução ocupação | Gráfico de linha |
| Distribuição leitos | Gráfico de barras |
| Meta vs. Real | Gauge |
| Readmissões por especialidade | Heatmap |
| Tempo de espera | Boxplot ou barras |
| Custo por procedimento | Treemap |
| Decomposição de variância | Decomposition Tree |

---

## Formatação Condicional

### Cores por Faixa de Ocupação

```dax
Cor Fundo Ocupação = 
SWITCH(
    TRUE(),
    [Taxa Ocupação] < 0.75, "#2d8a2d",  // Verde
    [Taxa Ocupação] < 0.85, "#aaaa2d",  // Amarelo
    [Taxa Ocupação] < 0.90, "#d98a2d",  // Laranja
    "#d92d2d"                           // Vermelho
)
```

### Ícones de Status

```dax
Status Meta = 
SWITCH(
    TRUE(),
    [Taxa Ocupação] <= [Meta Ocupação] * 0.9, "🟢",
    [Taxa Ocupação] <= [Meta Ocupação], "🟡",
    [Taxa Ocupação] <= [Meta Ocupação] * 1.1, "🟠",
    "🔴"
)
```

---

## Dicas de Performance

1. **Use Import Mode** para a maioria dos dados
2. **DirectQuery** apenas para dados em tempo real
3. **Incremental Refresh** para grandes volumes históricos
4. **Evite colunas não utilizadas** no modelo
5. **Otimize medidas DAX** com variáveis

---

## Atalhos Úteis

| Ação | Atalho |
|------|--------|
| Duplicar visual | Ctrl + D |
| Selecionar múltiplos | Shift + Clique |
| Agrupar | Ctrl + G |
| Alinhar | Ferramentas de Formato |
| Atualizar dados | F5 |

---

## Recursos Adicionais

- [Documentação oficial Power BI](https://docs.microsoft.com/power-bi/)
- [DAX Guide](https://dax.guide/)
- [SQL BI](https://www.sqlbi.com/)
- [Power BI Community](https://community.powerbi.com/)