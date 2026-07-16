# 🧪 Guia de Testes - Dashboard Hospitalar

Este documento descreve a estratégia de testes e como executar cada tipo de teste.

## 📋 Visão Geral

O projeto utiliza **pytest** como framework de testes, com foco em:

- **Testes Unitários**: Funções utilitárias e cálculos de negócio
- **Testes de Integração**: Integração com dados e visualizações
- **Testes E2E**: Fluxo completo do dashboard

## 🚀 Execução Rápida

```bash
# Todos os testes
pytest

# Com coverage
pytest --cov=src/web --cov-report=html

# Testes específicos
pytest tests/test_utils.py -v

# Testes com markadores
pytest -m unit
pytest -m smoke
```

## 📁 Estrutura de Testes

```
tests/
├── __init__.py              # Inicialização do pacote
├── test_utils.py            # Testes de utilitários
├── test_app.py              # Testes do app Streamlit (TODO)
└── conftest.py              # Fixtures compartilhadas (TODO)
```

## 🧪 Tipos de Testes

### 1. Testes Unitários (`-m unit`)

Testam funções individuais isoladamente.

```python
# Exemplo
def test_calcular_taxa_ocupacao():
    assert calcular_taxa_ocupacao(80, 100) == 80.0
```

**O que testar**:
- Funções de cálculo (taxa ocupação, giro leitos, etc.)
- Funções de formatação (moeda, percentual)
- Funções de validação
- Classificadores

### 2. Testes de Integração (`-m integration`)

Testam interação entre componentes.

**O que testar** (TODO):
- Carregamento de dados CSV
- Integração com DataFrame Pandas
- Geração de gráficos Plotly

### 3. Testes de Smoke (`-m smoke`)

Testes rápidos para validação pré-commit.

```bash
# Executa em < 5 segundos
pytest -m smoke --tb=short
```

### 4. Testes E2E (TODO)

Testam fluxo completo do dashboard.

**Ferramenta sugerida**: Playwright + pytest-playwright

## 📊 Coverage (Cobertura de Testes)

### Meta Mínima: 80%

```bash
# Verificar coverage
pytest --cov=src/web --cov-fail-under=80

# Gerar relatório HTML
pytest --cov=src/web --cov-report=html
# Abrir: open htmlcov/index.html
```

### Report de Coverage

```
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/web/utils.py         85      5    94%   45-48, 92, 156
src/web/app.py          150     20    87%   120-125, 245-250
---------------------------------------------------
TOTAL                   235     25    89%
```

## 🔧 Configuração

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --tb=short --cov=src/web
```

### Conftest.py (Fixtures)

```python
import pytest
import pandas as pd

@pytest.fixture
def dados_ocupacao_exemplo():
    return pd.DataFrame({
        'Data': pd.date_range('2024-01-01', periods=10),
        'Ocupacao': [80, 82, 85, 78, 90, 88, 84, 81, 79, 83],
    })
```

## 🐛 Debug de Testes

```bash
# Ver output de print
pytest -s

# Parar no primeiro erro
pytest -x

# Rodar último teste falho
pytest --lf

# Ver mais contexto no erro
pytest --tb=long
```

## 📈 Boas Práticas

### 1. Nomeclatura

```python
def test_<funcao>_<cenario>_<resultado_esperado>():
    # Exemplo
    def test_calcular_taxa_ocupacao_divisao_por_zero_retorna_zero():
        ...
```

### 2. Arrange-Act-Assert

```python
def test_exemplo():
    # Arrange (Preparação)
    valor = 100
    divisor = 0

    # Act (Execução)
    resultado = calcular_divisao(valor, divisor)

    # Assert (Verificação)
    assert resultado == 0
```

### 3. Testes Independentes

Cada teste deve:
- Não depender de outros testes
- Limpar seus próprios dados
- Ser executável isoladamente

## 🚨 Problemas Comuns

### Import Error

```bash
# Erro: ModuleNotFoundError
# Solução: Adicionar ao path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### Fixture não encontrada

```bash
# Erro: fixture 'nome' not found
# Solução: Verificar se conftest.py está no lugar certo
```

## 🔗 Integração CI/CD

O pipeline do GitHub Actions executa automaticamente:

1. Instala dependências
2. Roda linters (flake8, black, isort)
3. Executa testes com coverage
4. Upload do coverage para Codecov
5. Build Docker (após testes)

## 📝 Checklist Pré-Commit

- [ ] Testes unitários passam
- [ ] Coverage ≥ 80%
- [ ] Linters passam (flake8, black)
- [ ] Type checking passa (mypy)

## 🔮 Melhorias Futuras (TODO)

- [ ] Testes de integração com arquivos CSV reais
- [ ] Testes E2E com Playwright
- [ ] Testes de performance (pytest-benchmark)
- [ ] Testes de acessibilidade (axe-core)
- [ ] Implementar conftest.py com fixtures
- [ ] Testes desnapshot para gráficos

---

**Responsável**: Wellington de Lima Catarina
**Última atualização**: 2026-07-15