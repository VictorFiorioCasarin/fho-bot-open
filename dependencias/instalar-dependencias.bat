@echo off
title FHO Bot - Instalação Completa de Dependências
color 0A
echo.
echo ========================================
echo 🔧 FHO Bot - Instalação de Dependências
echo ========================================
echo.
echo � Verificando sistema...

:: Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo.
    echo Por favor, instale Python primeiro:
    echo https://python.org/downloads
    echo.
    echo Pressione qualquer tecla para sair.
    pause >nul
    exit /b 1
)

echo ✅ Python encontrado!

:: Verificar se pip está disponível
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip não encontrado!
    echo.
    echo Instalando pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo ❌ Falha ao instalar pip!
        pause >nul
        exit /b 1
    )
)

echo ✅ pip encontrado!
echo.

:: Atualizar pip para a versão mais recente
echo 📦 Atualizando pip...
python -m pip install --upgrade pip
echo.

:: Verificar se requirements.txt existe
if not exist "requirements.txt" (
    echo ❌ Arquivo requirements.txt não encontrado!
    echo.
    echo Certifique-se de estar na pasta correta do projeto.
    echo.
    pause >nul
    exit /b 1
)

echo 📋 Arquivo requirements.txt encontrado!
echo.

echo ========================================
echo 📦 INSTALANDO DEPENDÊNCIAS OTIMIZADAS...
echo ========================================
echo.
echo ✨ Lista completa e otimizada - incluindo BeautifulSoup4
echo 📦 Todas as dependências necessárias para o funcionamento
echo ⏳ Isso deve ser mais rápido que antes...
echo ⏳ Por favor, aguarde...
echo.

:: Instalar dependências com verbose para mostrar progresso
pip install -r requirements.txt --upgrade --verbose

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!
    echo ========================================
    echo.
    echo 🎉 Todas as dependências foram instaladas!
    echo.
    echo 📝 PRÓXIMOS PASSOS:
    echo.
    echo 1. Certifique-se de que o Ollama está instalado e rodando
    echo    💡 Download: https://ollama.ai
    echo.
    echo 2. Execute o modelo necessário no Ollama:
    echo    ollama pull deepseek-r1:8b
    echo.
    echo 3. Execute o bot:
    echo    🖥️  fhobot.bat - Interface gráfica
    echo    📝  fhobot-text.bat - Modo texto
    echo.
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ❌ ERRO NA INSTALAÇÃO!
    echo ========================================
    echo.
    echo 🔍 Possíveis soluções:
    echo.
    echo 1. Execute como Administrador
    echo 2. Verifique sua conexão com a internet
    echo 3. Atualize o Python para a versão mais recente
    echo 4. Tente executar manualmente:
    echo    pip install -r requirements.txt
    echo.
    echo 📞 Se o problema persistir, verifique:
    echo    - Firewall/Antivirus bloqueando
    echo    - Proxy corporativo
    echo    - Versão do Python (requer 3.8+)
    echo.
    echo ========================================
)

echo.
echo Pressione qualquer tecla para fechar.
pause >nul
