# Makefile para Dashboard Hospitalar
# =============================================================================
# Uso: make <comando>
# Exemplo: make test
# =============================================================================

.PHONY: help install dev test lint format clean run docker-build docker-run

# =============================================================================
# Comandos Principais
# =============================================================================

help: ## 📚 Mostrar ajuda com todos os comandos
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# =============================================================================
# Instalação e Setup
# =============================================================================

install: ## 📦 Instalar dependências de produção
	pip install -r src/web/requirements.txt

install-dev: ## 🛠️ Instalar dependências de desenvolvimento
	pip install -r requirements-dev.txt
	pip install -r src/web/requirements.txt

venv: ## 🐍 Criar ambiente virtual
	python -m venv venv
	@echo "Ative com: venv\\Scripts\\activate (Windows) ou source venv/bin/activate (Unix)"

# =============================================================================
# Testes e Qualidade
# =============================================================================

test: ## 🧪 Executar testes unitários
	pytest tests/ -v

test-cov: ## 📊 Executar testes com coverage
	pytest tests/ -v --cov=src/web --cov-report=html --cov-report=term-missing

test-fast: ## ⚡ Executar testes rápidos (smoke tests)
	pytest tests/ -v -m smoke

lint: ## 🔍 Executar linters
	flake8 src/ tests/ --max-line-length=100
	isort --check-only src/ tests/
	black --check src/ tests/

format: ## 🎨 Formatar código
	black src/ tests/
	isort src/ tests/

type-check: ## 🔎 Verificação de tipos
	mypy src/ --ignore-missing-imports

quality: lint type-check ## ✅ Executar todas as verificações de qualidade

# =============================================================================
# Execução
# =============================================================================

run: ## 🚀 Executar dashboard Streamlit
	streamlit run src/web/app.py

run-prod: ## 🌐 Executar em modo produção
	STREAMLIT_SERVER_HEADLESS=true streamlit run src/web/app.py

etl: ## 📊 Gerar dados de exemplo
	python src/etl/pacientes_etl.py

# =============================================================================
# Docker
# =============================================================================

docker-build: ## 🐳 Build da imagem Docker
	docker build -t dashboard-hospitalar:latest .

docker-run: ## 🏃 Executar container Docker
	docker run -p 8501:8501 dashboard-hospitalar:latest

docker-shell: ## 💻 Shell dentro do container
	docker run -it --rm dashboard-hospitalar:latest /bin/bash

# =============================================================================
# Limpeza
# =============================================================================

clean: ## 🧹 Limpar arquivos temporários
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.pyc" -exec rm -rf {} +

clean-all: clean ## 🧹🔥 Limpeza completa (inclui venv)
	rm -rf venv/

# =============================================================================
# Git e Versionamento
# =============================================================================

git-status: ## 📊 Mostrar status do git
	git status --short

git-pull: ## 📥 Git pull
	git pull origin main

git-push: ## 📤 Git push
	git push origin main

commit-all: ## 💾 Git add e commit
	git add .
	git commit -m "chore: atualização automática"

# =============================================================================
# Utilitários
# =============================================================================

check: quality test-fast ## ✅ Verificação rápida pré-commit

full-check: quality test-cov ## ✅✅ Verificação completa

tree: ## 🌳 Mostrar estrutura do projeto
	tree -I '__pycache__|venv|node_modules' -L 3

list-files: ## 📄 Listar todos os arquivos do projeto
	find . -type f \
		-not -path '*/\.*' \
		-not -path '*/__pycache__/*' \
		-not -path '*/venv/*' \
		-not -path '*/node_modules/*'

# =============================================================================
# Desenvolvimento
# =============================================================================

dev: install-dev format lint ## 🛠️ Setup completo para desenvolvimento

reset: clean-all venv install-dev ## 🔄 Resetar ambiente completo

# =============================================================================
# Documentação
# =============================================================================

docs-deps: ## 📚 Instalar dependências de documentação
	pip install mkdocs mkdocs-material mkdocstrings

docs-serve: ## 🌐 Servir documentação localmente
	mkdocs serve

docs-build: ## 📦 Build da documentação
	mkdocs build