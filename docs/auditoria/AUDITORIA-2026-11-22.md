# Auditoria — 2026-11-22

**Repositório:** Lelolima/Sess-o-Power-BI-
**Finalidade real:** portfólio de BI hospitalar. A parte executável é um dashboard Streamlit (`src/web/app.py`) com **dados sintéticos** e um script ETL que gera CSVs sintéticos. Não há arquivo `.pbix` nem dados reais no repositório (o README antigo dizia que havia).
**Stack:** Python 3.11+, Streamlit, pandas, numpy, plotly; pytest; Docker.

## Estado anterior
- CI (`CI/CD Pipeline`, run 29519714092) falhando em 2 jobs. Os logs já expiraram (HTTP 410), então a causa foi reproduzida localmente:
  - **Testes:** `tests/__init__.py` tinha docstring sem abertura → `SyntaxError` na coleta; nenhum teste rodava.
  - **Security Scan:** usava `actions/upload-artifact@v3`, descontinuada pelo GitHub (os jobs com v3 falham de forma automática).
- Depois de corrigir a coleta: 4 testes falhando (`formatar_numero` → `ValueError`; `calcular_variacao` não existia, só `calcular_variação`) e cobertura de 33% (mínimo exigido: 80%).
- O workflow tinha jobs de push para GHCR e de "deploy", e não declarava permissões.

## Problemas encontrados

| # | Sev. | Problema | Evidência | Correção |
|---|------|----------|-----------|----------|
| 1 | P1 | Testes não eram coletados | `SyntaxError: unterminated triple-quoted string literal` em `tests/__init__.py` | Docstring corrigida |
| 2 | P1 | CI quebrado (artifact v3, testes) | Run 29519714092 | Workflow novo e enxuto |
| 3 | P1 | `formatar_numero` sempre levantava exceção | `ValueError: Format specifier missing precision` | Separador aplicado via `replace` |
| 4 | P2 | Testes chamavam `calcular_variacao`, que não existia | `NameError` | Alias ASCII; o nome original foi mantido |
| 5 | P1 | KPIs "Giro de Leitos" e "Tempo Médio Espera" eram sorteados com `np.random` a cada renderização, com delta fixo "+0.3" (números simulados apresentados como métricas) | `criar_cards_kpis` | `calcular_kpis_operacionais` calcula os KPIs a partir dos dados carregados. A sidebar avisa que os dados são sintéticos |
| 6 | P1 | ETL quebrava ao rodar | `OSError: Cannot save file into a non-existent directory: 'data'` | `os.makedirs('data', exist_ok=True)` |
| 7 | P2 | `app.py` sem testes (0% de cobertura) | relatório de cobertura | Smoke tests reais com `streamlit.testing.AppTest` nas 4 páginas, mais teste de determinismo |
| 8 | P2 | Imports não usados, variável morta no ETL | ruff F401/F841 | Removidos |
| 9 | P3 | README descrevia arquivos que não existem (`.pbix`, CSVs, `cd src/web && streamlit run app.py`) | árvore do repo | README reescrito nas seções de estrutura e uso |

**Segredos:** nada encontrado. Busquei padrões de chaves (AWS, GitHub, OpenAI, Slack, Google e chaves privadas) na árvore atual e em todo o histórico (`git log -p --all`). gitleaks não está instalado na máquina, então a busca foi manual por regex.
**Dependências:** `pip-audit -r src/web/requirements.txt` → "No known vulnerabilities found".

## Testes executados (local, Windows, Python 3.13.15)
- `pytest` → **43 passed**, cobertura total de 95.72% (o mínimo de 80% foi atingido).
- `ruff check --select E9,F63,F7,F82,F401,F841 src tests` → sem erros.
- ETL executado num diretório temporário (`tests/test_etl.py`): gera os 4 CSVs.
- Build Docker: não rodei localmente. Ele é validado pelo job `build` do CI (resultado no PR).

## CI novo
`.github/workflows/ci.yml`: `permissions: contents: read`, actions fixadas por SHA, job lint+testes e job `docker build` sem push. Os jobs de push para GHCR e de deploy foram removidos (estavam fora do escopo).

## Riscos residuais / decisões do dono
- O job de publicação da imagem no GHCR foi removido. Se a publicação for desejada, crie um workflow de release separado com `packages: write`.
- Os KPIs de giro e tempo de espera continuam vindo de dados sintéticos. Agora são coerentes com o restante do dashboard, mas não representam um hospital real.
- O `Dockerfile` instala também `requirements-dev.txt` na imagem final (imagem maior). Não alterei.
- Vários arquivos de rascunho na raiz (`*.txt`, `enviar-github.bat`, relatórios antigos) foram mantidos. A remoção fica a critério do dono.
