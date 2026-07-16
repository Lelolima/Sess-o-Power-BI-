@echo off
REM =============================================================================
REM Script de Envio para GitHub - Dashboard Hospitalar Power BI
REM Repositório: https://github.com/Lelolima/Sess-o-Power-BI-
REM =============================================================================

cd /d "%~dp0"

echo.
echo =============================================================================
echo           ENVIANDO PROJETO PARA GITHUB
echo           Repositorio: Sess-o-Power-BI-
echo =============================================================================
echo.

REM Verifica se Git está instalado
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Git não está instalado ou não está no PATH!
    echo Baixe em: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo [1/8] Verificando status do repositório...
git status >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [2/8] Inicializando repositório Git...
    git init
) else (
    echo [2/8] Repositório já inicializado
)

echo.
echo [3/8] Adicionando todos os arquivos...
git add .

echo.
echo [4/8] Verificando arquivos para commit...
git status --short

echo.
set /p CONFIRM="Continuar com o commit? (S/N): "
if /i "%CONFIRM%" NEQ "S" (
    echo [INFO] Operação cancelada pelo usuário.
    pause
    exit /b 0
)

echo.
echo [5/8] Criando commit...
git commit -m "feat: projeto completo dashboard hospitalar Power BI

- Estrutura organizada com docs, src, tests, data, screenshots
- Dashboard web em Streamlit com 4 páginas
- 5 SVGs animados para demonstração
- 30+ testes unitários com pytest
- Docker e CI/CD configurados
- Documentação completa
- Datasets de exemplo anonimizados

Autor: Wellington de Lima Catarina <lelolima806@gmail.com>"

if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Nenhum arquivo para commit ou erro no commit.
)

echo.
echo [6/8] Renomeando branch para main...
git branch -M main 2>nul

echo.
echo [7/8] Configurando remote...
git remote remove origin 2>nul
git remote add origin https://github.com/Lelolima/Sess-o-Power-BI-.git

echo.
echo [8/8] Enviando para GitHub...
echo.
echo ================================================================
echo Atenção: Será solicitada autenticação no GitHub
echo - Use seu Personal Access Token se tiver 2FA habilitado
echo - Token: https://github.com/settings/tokens
echo ================================================================
echo.

git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =============================================================================
    echo [SUCESSO] Projeto enviado para GitHub!
    echo.
    echo Acesse: https://github.com/Lelolima/Sess-o-Power-BI-
    echo =============================================================================
) else (
    echo.
    echo =============================================================================
    echo [ERRO] Falha ao enviar. Verifique:
    echo - Você tem permissão no repositório?
    echo - Autenticação está configurada?
    echo - Remote URL está correta?
    echo.
    echo Tente manualmente: git push -u origin main
    echo =============================================================================
)

echo.
pause