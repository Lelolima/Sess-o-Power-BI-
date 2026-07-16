# Guia de Contribuição

Obrigado por contribuir com este projeto! 🎉

Este documento estabelece diretrizes e padrões para contribuir com o Dashboard Hospitalar Power BI.

## Como Contribuir

### 1. Reportando Bugs

Se você encontrou um bug, por favor crie uma issue no GitHub incluindo:

- Uma descrição clara e descritiva
- Passos para reproduzir o problema
- Comportamento esperado vs. comportamento atual
- Screenshots (se aplicável)
- Informações do ambiente (versão do Power BI, SO, etc.)

### 2. Sugerindo Melhorias

Sugestões são bem-vindas! Por favor crie uma issue incluindo:

- Uma descrição clara da melhoria
- Contexto e justificativa
- Exemplos de uso
- Alternativas consideradas (se houver)

### 3. Pull Requests

Para submeter mudanças:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona minha feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### 4. Padrões de Código

**Para arquivos DAX**:
- Use nomes descritivos para medidas
- Inclua comentários para lógica complexa
- Formate com indentação consistente

**Para scripts Python**:
- Siga PEP 8
- Inclua docstrings
- Adicione type hints quando apropriado

**Para documentação**:
- Use Markdown
- Mantenha linguagem clara e objetiva
- Inclua exemplos quando aplicável

### 5. Estrutura de Pastas

```
├── dashboards/      # Arquivos .pbix
├── data/           # Datasets de exemplo
├── docs/           # Documentação técnica
├── screenshots/    # Imagens
├── src/            # Código fonte
│   ├── etl/       # Scripts Python ETL
│   └── web/       # Versão web (Streamlit)
```

## Código de Conduta

Este projeto segue o [Código de Conduta](CODE_OF_CONDUCT.md). Por favor, leia antes de contribuir.

## Licenciamento

Ao contribuir, você concorda que suas contribuições estejam sob a mesma licença MIT do projeto.

## Dúvidas?

Entre em contato: lelolima806@gmail.com ou abra uma issue no GitHub.