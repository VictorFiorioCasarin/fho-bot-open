#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FHO Bot com Interface Visual
Versão visual integrada do assistente FHO
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
import yaml
import threading
import re
import time

# Importar módulos do bot
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from speech_to_text import SpeechToText
from text_to_speech.tts_manager import TTSManager
from rag_pipeline import get_context
from visual_interface import VisualInterface, BotState

class FHOBotVisual:
    """Bot FHO com interface visual integrada"""
    
    def __init__(self):
        """Inicializa o bot visual"""
        # Carregar configurações
        with open("config.yaml", "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)
        
        # Configurar modelo LLM
        self.setup_llm()
        
        # Carregar prompt principal
        with open("prompts/main_prompt.yaml", "r", encoding="utf-8") as file:
            self.main_prompt = yaml.safe_load(file)['prompt']
        
        # Inicializar componentes de voz
        self.speech_to_text = SpeechToText()
        self.tts = TTSManager()
        
        # Criar interface visual
        self.interface = VisualInterface(
            on_text_input=self.handle_text_input,
            on_voice_input=self.handle_voice_input
        )
        
        # Estado de processamento
        self.processing = False
    
    def setup_llm(self):
        """Configura o modelo LLM"""
        # Modelos disponíveis
        MODELS = {
            "deepseek": "deepseek-r1:8b",
            "deepseek7b": "deepseek-r1:7b", 
            "gemma3": "gemma3:4b"
        }
        
        # Configurar modelo baseado no config
        model_name = self.config['modelo']
        if model_name not in MODELS:
            print(f"Erro: Modelo '{model_name}' não encontrado. Usando deepseek como padrão.")
            model_name = "deepseek"
        
        model_llm = MODELS[model_name]
        
        self.llm = ChatOllama(
            model=model_llm,
            temperature=self.config['llm']['temperatura'],
        )
    
    def handle_text_input(self, text: str):
        """
        Processa entrada de texto do usuário
        
        Args:
            text: Texto digitado pelo usuário
        """
        if self.processing:
            self.interface.add_message("system", "Aguarde, ainda estou processando a mensagem anterior...")
            return
        
        if text.lower() == 'exit':
            self.handle_exit()
            return
        
        # Mostrar mensagem do usuário
        self.interface.add_message("user", text)
        
        # Processar mensagem
        self.process_message(text)
    
    def handle_voice_input(self):
        """Processa entrada de voz do usuário"""
        if self.processing:
            self.interface.add_message("system", "Aguarde, ainda estou processando a mensagem anterior...")
            return
        
        try:
            # Mudar para estado de escuta
            self.interface.set_state(BotState.LISTENING)
            
            # Capturar entrada de voz
            user_input = self.speech_to_text.get_voice_input()
            
            if user_input is None:
                self.interface.set_state(BotState.IDLE)
                self.interface.add_message("system", "Nenhuma entrada de voz detectada.")
                return
            
            if user_input.lower() == 'exit':
                self.handle_exit()
                return
            
            # Mostrar transcrição
            self.interface.add_message("user", f"🎤 {user_input}")
            
            # Processar mensagem
            self.process_message(user_input)
            
        except Exception as e:
            self.interface.set_state(BotState.IDLE)
            self.interface.add_message("system", f"Erro na captura de voz: {e}")
    
    def process_message(self, user_input: str):
        """
        Processa mensagem do usuário (texto ou voz)
        
        Args:
            user_input: Entrada do usuário
        """
        self.processing = True
        
        try:
            # Estado: Pensando (processando LLM)
            self.interface.set_state(BotState.THINKING)
            
            # Obter contexto da RAG
            context = get_context(user_input)
            
            # Preparar mensagens para o LLM
            messages = [
                SystemMessage(content=f"{self.main_prompt}\n\nContexto:\n{context}"),
                HumanMessage(content=user_input)
            ]
            
            # Processar com LLM
            response = self.llm.invoke(messages)
            
            # Filtrar o <think> do DeepSeek-R1
            response_content = response.content
            if '<think>' in response_content and '</think>' in response_content:
                response_content = re.sub(r'<think>.*?</think>', '', response_content, flags=re.DOTALL).strip()
            
            # Estado: Falando (TTS ativo)
            self.interface.set_state(BotState.SPEAKING)
            
            # Mostrar resposta
            self.interface.add_message("bot", response_content)
            
            # Falar resposta (se TTS habilitado)
            if self.tts.is_available():
                self.tts.speak(response_content)
            
            # Voltar ao estado neutro
            self.interface.set_state(BotState.IDLE)
            
        except Exception as e:
            # Em caso de erro
            self.interface.set_state(BotState.IDLE)
            error_message = f"Erro ao processar mensagem: {e}"
            self.interface.add_message("system", error_message)
            
            if self.tts.is_available():
                self.tts.speak("Desculpe, ocorreu um erro. Tente novamente.")
        
        finally:
            self.processing = False
    
    def handle_exit(self):
        """Trata comando de saída"""
        farewell_message = "Adeus! Foi um prazer conversar com você!"
        self.interface.add_message("bot", farewell_message)
        
        if self.tts.is_available():
            self.interface.set_state(BotState.SPEAKING)
            self.tts.speak(farewell_message)
            time.sleep(2)  # Aguardar fala terminar
        
        self.interface.close()
    
    def run(self):
        """Inicia o bot visual"""
        print("🤖 Iniciando FHO Bot com Interface Visual...")
        print(f"🎯 TTS: {self.tts.get_simple_info()}")
        print(f"🎤 STT: {self.speech_to_text.get_welcome_message()}")
        
        # Falar mensagem de boas-vindas
        welcome_message = "Olá! Eu sou seu assistente. Estou aqui para conversar com você sobre o curso de Engenharia de Computação da FHO!"
        if self.tts.is_available():
            self.tts.speak(welcome_message)
        
        # Iniciar interface visual
        self.interface.run()

if __name__ == "__main__":
    # Criar e executar bot visual
    bot = FHOBotVisual()
    bot.run()
