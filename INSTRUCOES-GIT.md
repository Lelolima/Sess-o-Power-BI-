# 📦 Instruções para Commit Inicial

## Passo a Passo

### 1. Mover Arquivos Originais (Opcional)

Mova os arquivos de texto originais para a pasta `_referencias/`:
- `Sess-o-Power-BI.txt`
- `Instruções para as correções de projeto BI.txt`

### 2. Inicializar Repositório Git

```bash
cd "C:\Users\Thinkin pad 8g\Desktop\Sess-o-power-BI"

# Inicializar repositório
git init

# Adicionar todos os arquivos
git add .

# Verificar status
git status
```

### 3. Commit Inicial

```bash
git commit -m "feat: estrutura inicial do portfólio BI - Dashboard Hospitalar

- Estrutura de pastas organizada (dashboards, data, docs, src)
- README.md versão elite com badges e métricas
- Documentação técnica (arquitetura, DAX, estudo de caso)
- Scripts Python ETL e versão web Streamlit
- Datasets de exemplo anonimizados
- Arquivos de profissionalismo (LICENSE, CODE_OF_CONDUCT, CONTRIBUTING)
- Roadmap do projeto

Ref: github.com/Lelolima/Sess-o-Power-BI-"
```

### 4. Renomear Repositório (Recomendado)

No GitHub:
1. Vá em Settings do repositório
2. Renomeie para: `portfolio-bi-wellington-lima`
3. Ou: `dashboard-hospitalar-powerbi-analytics`

### 5. Push para GitHub

```bash
# Adicionar remote (após criar novo repo)
git remote add origin https://github.com/Lelolima/portfolio-bi-wellington-lima.git

# Fazer push
git branch -M main
git push -u origin main
```

### 6. Atualizar Links no README

Edite `README.md` e atualize:
- URL do repositório
- URL do deploy (após deploy)
- Qualquer link quebrado

---

## 🚀 Deploy da Versão Web

### Netlify

1. Crie conta em [netlify.com](https://netlify.com)
2. Conecte seu repositório GitHub
3. Configure:
   - Build command: `pip install -r src/web/requirements.txt`
   - Publish directory: `src/web`
   - Start command: `streamlit run app.py`

### Render

1. Crie conta em [render.com](https://render.com)
2. New Web Service
3. Conecte repositório
4. Configure:
   - Build: `pip install -r src/web/requirements.txt`
   - Start: `streamlit run src/web/app.py`

---

## ✅ Checklist Final

- [ ] Git inicializado
- [ ] Commit inicial feito
- [ ] Repositório renomeado
- [ ] Push realizado
- [ ] README atualizado
- [ ] Deploy web configurado
- [ ] Screenshots adicionadas
- [ ] Arquivo .pbix criado

---

**Tempo estimado:** 30 minutos
**Dificuldade:** Iniciante