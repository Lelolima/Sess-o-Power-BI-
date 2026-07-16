# 🚀 Getting Started - Dashboard Hospitalar Power BI

Este guia inclui instruções passo a passo para configurar e executar este projeto localmente.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Power BI Desktop](https://powerbi.microsoft.com/downloads/) (versão mais recente)
- [Python 3.11+](https://python.org/downloads) (para scripts ETL e versão web)
- [Git](https://git-scm.com/downloads)

## 🔧 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/Lelolima/portfolio-bi-wellerson-lima.git
cd portfolio-bi-wellerson-lima
```

### 2. Instale as Dependências Python

```bash
# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r src/web/requirements.txt
```

## 📊 Executando o Projeto

### Opção 1: Power BI Desktop

1. Abra o Power BI Desktop
2. Vá em `Arquivo` > `Abrir Relatório`
3. Navegue até `dashboards/Dashboard-Hospitalar.pbix`
4. Clique em `Atualizar` para carregar os dados

### Opção 2: Scripts ETL (Python)

```bash
# Gerar datasets de exemplo
cd src/etl
python pacientes_etl.py
```

Os dados serão salvos em `data/`.

### Opção 3: Versão Web (Streamlit)

```bash
# Navegue até a pasta web
cd src/web

# Execute o app
streamlit run app.py
```

O dashboard abrirá automaticamente no seu navegador em `http://localhost:8501`.

## 📁 Estrutura de Arquivos

```
portfolio-bi-wellerson-lima/
├── README.md                 # documentação principal
├── GETTING_STARTED.md        # este arquivo
├── CONTRIBUTING.md           # guia de contribuição
├── CODE_OF_CONDUCT.md        # código de conduta
├── LICENSE                   # licença MIT
├── .gitignore                # arquivos ignorados pelo git
│
├── dashboards/               # arquivos Power BI
│   └── Dashboard-Hospitalar.pbix
│
├── data/                     # datasets de exemplo
│   ├── pacientes_sample.csv
│   ├── internacoes_sample.csv
│   ├── medicos_sample.csv
│   └── leitos_sample.csv
│
├── docs/                     # documentação técnica
│   ├── arquitetura.md
│   ├── estudo-de-caso-hospitalar.md
│   ├── medidas-dax.md
│   └── roadmap.md
│
├── screenshots/              # imagens do dashboard
│
└── src/                      # código fonte
    ├── etl/
    │   └── pacientes_etl.py
    └── web/
        ├── app.py
        └── requirements.txt
```

## 🎯 Próximos Passos

1. **Explore o dashboard** no Power BI Desktop
2. **Personalize** as medidas DAX conforme sua necessidade
3. **Conecte** a suas próprias fontes de dados
4. **Publique** no Power BI Service para compartilhamento

## ❓ Problemas Comuns

### "Não consigo abrir o arquivo .pbix"
Certifique-se de usar a versão mais recente do Power BI Desktop.

### "Dados não carregam"
Verifique se os arquivos CSV estão na pasta `data/` e tente atualizar as credenciais da fonte de dados.

### "Streamlit não inicia"
Verifique a instalação: `pip list | findstr streamlit`

## 🤝 Precisa de Ajuda?

- Abra uma [issue](https://github.com/Lelolima/portfolio-bi-wellerson-lima/issues)
- Entre em contato: lelolima806@gmail.com
- LinkedIn: [Wellington Lima](https://www.linkedin.com/in/wellington-de-lima-catarina/)