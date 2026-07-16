# 🚀 Guia de Deploy - Dashboard Hospitalar

Este guia cobre todas as opções de deployment para o dashboard.

## 📋 Pré-requisitos

- Conta no GitHub
- Python 3.11+ instalado localmente
- Docker (opcional, para deploy local)

---

## ☁️ Opção 1: Streamlit Cloud (Recomendado - Gratuito)

### Vantagens
- ✅ Gratuito para projetos públicos
- ✅ Deploy automático ao fazer push
- ✅ HTTPS incluído
- ✅ ≠ configuração de servidor

### Passos

1. **Acesse** [share.streamlit.io](https://share.streamlit.io)

2. **Conecte** sua conta GitHub

3. **Selecione** o repositório:
   ```
   Repository: Lelolima/portfolio-bi-wellington-lima
   Branch: main
   Main file path: src/web/app.py
   ```

4. **Configure** variáveis de ambiente (Settings > Secrets):
   ```
   STREAMLIT_SERVER_PORT=8501
   ```

5. **Clique** em "Deploy!"

6. **Aguarde** ~2-5 minutos para o primeiro deploy

### Custom Domain (Opcional)

```bash
# No Streamlit Cloud: Settings > Custom Domain
# Adicione registro CNAME no seu DNS:
CNAME streamlit.io
```

**Tempo estimado**: 10 minutos
**Custo**: Gratuito

---

## 🚂 Opção 2: Render.com

### Vantagens
- ✅ Plano gratuito disponível
- ✅ Deploy automático do GitHub
- ✅ Suporte a Docker

### Passos

1. **Acesse** [render.com](https://render.com)

2. **New Web Service** → Connect GitHub

3. **Configure**:
   ```
   Name: hospital-dashboard
   Region: Oregon (us-east-1)
   Branch: main
   Root Directory: (deixe vazio)
   Runtime: Python 3
   Build Command: pip install -r src/web/requirements.txt
   Start Command: streamlit run src/web/app.py --server.port $PORT --server.address 0.0.0.0
   ```

4. **Environment Variables**:
   ```
   PYTHON_VERSION=3.11
   ```

5. **Deploy**

### render.yaml (IaC)

```yaml
services:
  - type: web
    name: hospital-dashboard
    env: python
    buildCommand: pip install -r src/web/requirements.txt
    startCommand: streamlit run src/web/app.py --server.port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
    healthCheckPath: /_stcore/health
```

**Tempo estimado**: 15 minutos
**Custo**: Gratuito (com limites) ou $7/mês

---

## 🚀 Opção 3: Railway.app

### Vantagens
- ✅ $5 de crédito gratuito
- ✅ Deploy muito rápido
- ✅ Variáveis de ambiente fáceis

### Passos

1. **Acesse** [railway.app](https://railway.app)

2. **New Project** → Deploy from GitHub repo

3. **Selecione** o repositório

4. **Variables**:
   ```
   PORT=8501
   PYTHON_VERSION=3.11.0
   ```

5. **Settings** → mude Root Directory para `src/web`

6. **Deploy**

**Tempo estimado**: 8 minutos
**Custo**: $5 crédito grátis, depois pay-as-you-go

---

## 🐳 Opção 4: Docker + VPS

### Para produção real com controle total

### Requisitos
- VPS (DigitalOcean, Linode, AWS EC2, etc.)
- Domínio configurado
- Conhecimento de Linux

### Deploy

```bash
# Na VPS
git clone https://github.com/Lelolima/portfolio-bi-wellington-lima.git
cd portfolio-bi-wellington-lima

# Copiar .env
cp .env.example .env

# Editar .env com suas credenciais
nano .env

# Deploy com Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f dashboard
```

### SSL com Let's Encrypt

```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx

#Gerar certificado
certbot --nginx -d seudominio.com

# Auto-renew
certbot renew --dry-run
```

**Tempo estimado**: 1-2 horas
**Custo**: $5-20/mês (VPS) + domínio

---

## 🌐 Opção 5: Vercel/Netlify (com adaptações)

### Para versão estática ou com backend serverless

### Adaptações necessárias

1. **Criar** `vercel.json`:
```json
{
  "version": 2,
  "builds": [{
    "src": "src/web/app.py",
    "use": "@vercel/python"
  }],
  "routes": [{
    "src": "/(.*)",
    "dest": "src/web/app.py"
  }]
}
```

2. **Requirements** específicos:
```
streamlit==1.30.0
pandas==2.0.0
plotly==5.17.0
numpy==1.24.0
```

3. **Deploy**:
```bash
vercel login
vercel --prod
```

**Limitação**: Streamlit não roda nativamente no Vercel. Considere migrar para Dash ou Flask.

---

## 📊 Comparação de Opções

| Plataforma | Custo | Facilidade | Performance | Recomendado para |
|------------|-------|------------|-------------|------------------|
| Streamlit Cloud | Free | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Portfólio, Demo |
| Render | Free/$7 | ⭐⭐⭐⭐ | ⭐⭐⭐ | Produção leve |
| Railway | $5 credit | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | MVP, Produção |
| Docker + VPS | $5-20/mês | ⭐⭐ | ⭐⭐⭐⭐⭐ | Produção real |
| Vercel | Free | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Apps estáticos |

---

## 🔧 Troubleshooting

### Build falha no Streamlit Cloud

```
Error: No module named 'pandas'
```

**Solução**: Verifique se `requirements.txt` está na raiz ou especifique caminho correto.

### App fica offline após deploy

**Solução**: 
1. Verifique logs: `docker-compose logs dashboard`
2. Teste health check: `curl http://localhost:8501/_stcore/health`
3. Verifique portas: `docker ps`

### Dados não carregam

**Solução**:
1. Verifique paths relativos no código
2. Dados devem estar em pasta acessível
3. Monte volume no Docker: `-v ./data:/app/data`

---

## 📈 Próximos Passos após Deploy

1. **Configurar domínio customizado** (opcional)
2. **Adicionar analytics** (Google Analytics, Plausible)
3. **Configurar alerts** (UptimeRobot, StatusCake)
4. **Setup CI/CD** (GitHub Actions)
5. **Documentar** URL no README e LinkedIn

---

**Suporte**: Para problemas, abra issue no GitHub ou contate lelolima806@gmail.com