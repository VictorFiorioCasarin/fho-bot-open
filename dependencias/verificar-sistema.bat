@echo off
title FHO Bot - Verificação do Sistema
color 0B
echo.
echo ========================================
echo 🔍 FHO Bot - Verificação do Sistema
echo ========================================
echo.

echo 🐍 PYTHON:
echo ----------------------------------------
python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado
) else (
    echo ✅ Python instalado
)
echo.

echo 📦 PIP:
echo ----------------------------------------
pip --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ pip não encontrado
) else (
    echo ✅ pip instalado
)
echo.

echo 🤖 OLLAMA:
echo ----------------------------------------
ollama --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Ollama não encontrado
    echo 💡 Baixe em: https://ollama.ai
) else (
    echo ✅ Ollama instalado
    echo.
    echo 📋 Modelos disponíveis:
    ollama list 2>nul
)
echo.

echo 📁 ARQUIVOS DO PROJETO:
echo ----------------------------------------
if exist "main.py" (
    echo ✅ main.py encontrado
) else (
    echo ❌ main.py não encontrado
)

if exist "config.yaml" (
    echo ✅ config.yaml encontrado
) else (
    echo ❌ config.yaml não encontrado
)

if exist "requirements.txt" (
    echo ✅ requirements.txt encontrado
) else (
    echo ❌ requirements.txt não encontrado
)

if exist "Tkinter\main_enhanced.py" (
    echo ✅ Interface gráfica encontrada
) else (
    echo ❌ Interface gráfica não encontrada
)
echo.

echo 📚 DEPENDÊNCIAS PYTHON PRINCIPAIS:
echo ----------------------------------------
echo 🔍 Verificando bibliotecas instaladas...
echo.

python -c "import langchain_ollama; print('✅ langchain-ollama')" 2>nul || echo "❌ langchain-ollama"
python -c "import speech_recognition; print('✅ speech_recognition')" 2>nul || echo "❌ speech_recognition"
python -c "import yaml; print('✅ PyYAML')" 2>nul || echo "❌ PyYAML"
python -c "import chromadb; print('✅ chromadb')" 2>nul || echo "❌ chromadb"
python -c "import azure.cognitiveservices.speech; print('✅ azure-cognitiveservices-speech')" 2>nul || echo "❌ azure-cognitiveservices-speech"
python -c "import pyaudio; print('✅ pyaudio')" 2>nul || echo "❌ pyaudio"
python -c "import pygame; print('✅ pygame')" 2>nul || echo "❌ pygame"
python -c "import bs4; print('✅ beautifulsoup4 (bs4)')" 2>nul || echo "❌ beautifulsoup4 (bs4)"
python -c "import tkinter; print('✅ tkinter (nativo)')" 2>nul || echo "❌ tkinter (nativo)"

echo.
echo ========================================
echo 📊 RESUMO:
echo ========================================
echo.
echo Se algum item estiver com ❌, execute:
echo 1. instalar-dependencias.bat
echo 2. Instale o Ollama se necessário
echo 3. Execute: ollama pull deepseek-r1:8b
echo.
echo ========================================
echo.
echo Pressione qualquer tecla para fechar.
pause >nul
