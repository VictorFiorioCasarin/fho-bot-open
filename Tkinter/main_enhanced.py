#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FHO Bot com Interface Visual Aprimorada
Versão final para apresentação na feira
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
from enhanced_visual import EnhancedVisualInterface, BotState

class FHOBotEnhanced:
    """Bot FHO com interface visual aprimorada para feira"""
    
    def __init__(self):
        """Inicializa o bot visual aprimorado"""
        # Carregar configurações (do diretório pai)
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)
        
        # Configurar modelo LLM
        self.setup_llm()
        
        # Carregar prompt principal (do diretório pai)
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "main_prompt.yaml")
        with open(prompt_path, "r", encoding="utf-8") as file:
            self.main_prompt = yaml.safe_load(file)['prompt']
        
        # Inicializar componentes de voz
        self.speech_to_text = SpeechToText()
        self.tts = TTSManager()
        
        # Criar interface visual aprimorada
        self.interface = EnhancedVisualInterface(
            on_text_input=self.handle_text_input,
            on_voice_input=self.handle_voice_input
        )
        
        # Estado de processamento
        self.processing = False
        
        # Atualizar status do TTS na interface
        self.interface.update_tts_status(self.tts.get_simple_info())
    
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
            print(f"Aviso: Modelo '{model_name}' não encontrado. Usando deepseek como padrão.")
            model_name = "deepseek"
        
        model_llm = MODELS[model_name]
        
        self.llm = ChatOllama(
            model=model_llm,
            temperature=self.config['llm']['temperatura'],
        )
        
        # Armazenar nome completo do modelo para exibição
        self.model_display_name = model_llm
    
    def handle_text_input(self, text: str):
        """
        Processa entrada de texto do usuário
        
        Args:
            text: Texto digitado pelo usuário
        """
        if self.processing:
            self.interface.add_message("system", "⏳ Aguarde, ainda estou processando a mensagem anterior...")
            return
        
        if text.lower() in ['exit', 'sair', 'tchau']:
            self.handle_exit()
            return
        
        # Mostrar mensagem do usuário
        self.interface.add_message("user", text)
        
        # Processar mensagem
        self.process_message(text)
    
    def handle_voice_input(self):
        """Processa entrada de voz do usuário"""
        if self.processing:
            self.interface.add_message("system", "⏳ Aguarde, ainda estou processando a mensagem anterior...")
            return
        
        try:
            # Mudar para estado de escuta
            self.interface.set_state(BotState.LISTENING)
            
            # Capturar entrada de voz
            user_input = self.speech_to_text.get_voice_input()
            
            if user_input is None:
                self.interface.set_state(BotState.IDLE)
                self.interface.add_message("system", "🎤 Nenhuma entrada de voz detectada. Tente novamente.")
                return
            
            if user_input.lower() in ['exit', 'sair', 'tchau']:
                self.handle_exit()
                return
            
            # Mostrar transcrição
            self.interface.add_message("user", f"🎤 \"{user_input}\"")
            
            # Processar mensagem
            self.process_message(user_input)
            
        except Exception as e:
            self.interface.set_state(BotState.IDLE)
            self.interface.add_message("system", f"❌ Erro na captura de voz: {e}")
    
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
            
            # Verificar se a resposta não está vazia
            if not response_content.strip():
                response_content = "Desculpe, não consegui processar sua pergunta adequadamente. Poderia reformular?"
            
            # Estado: Falando (TTS ativo)
            self.interface.set_state(BotState.SPEAKING)
            
            # Mostrar resposta
            self.interface.add_message("bot", response_content)
            
            # Falar resposta (se TTS habilitado)
            if self.tts.is_available():
                # Executar TTS em thread separada para não bloquear a interface
                threading.Thread(target=self._speak_response, args=(response_content,), daemon=True).start()
            else:
                # Se TTS não está disponível, voltar ao estado neutro imediatamente
                self.interface.set_state(BotState.IDLE)
            
        except Exception as e:
            # Em caso de erro
            self.interface.set_state(BotState.IDLE)
            error_message = f"❌ Erro ao processar mensagem: {str(e)[:100]}..."
            self.interface.add_message("system", error_message)
            
            if self.tts.is_available():
                self.tts.speak("Desculpe, ocorreu um erro. Tente novamente.")
        
        finally:
            self.processing = False
    
    def _speak_response(self, text: str):
        """
        Fala a resposta usando TTS (executado em thread separada)
        
        Args:
            text: Texto para ser falado
        """
        try:
            self.tts.speak(text)
        except Exception as e:
            print(f"Erro no TTS: {e}")
        finally:
            # Voltar ao estado neutro após falar
            self.interface.set_state(BotState.IDLE)
    
    def handle_exit(self):
        """Trata comando de saída"""
        farewell_message = "Adeus! Foi um prazer conversar com você sobre Engenharia de Computação! 🎓"
        self.interface.add_message("bot", farewell_message)
        
        if self.tts.is_available():
            self.interface.set_state(BotState.SPEAKING)
            # Falar despedida em thread separada
            def speak_and_close():
                try:
                    self.tts.speak(farewell_message)
                    time.sleep(1)  # Pequena pausa
                except:
                    pass
                finally:
                    self.interface.close()
            
            threading.Thread(target=speak_and_close, daemon=True).start()
        else:
            time.sleep(1)
            self.interface.close()
    
    def run(self):
        """Inicia o bot visual aprimorado"""
        print("\n" + "="*60)
        print("🤖 INICIANDO FHO BOT")
        print("="*60)
        print(f"🧠 Modelo LLM: {self.model_display_name}")
        print(f"🎯 Método TTS: {self.tts.get_simple_info()}")
        print(f"🎤 STT: {self.speech_to_text.get_stt_info()}")
        print(f"🌐 Interface: Tkinter")
        print("="*60)
        
        # Falar mensagem de boas-vindas
        welcome_message = ("Olá! Eu sou seu assistente virtual da FHO. "
                          "Estou aqui para conversar com você sobre o curso de Engenharia de Computação!")
        
        if self.tts.is_available():
            # Falar boas-vindas em thread para não bloquear a interface
            threading.Thread(target=self.tts.speak, args=(welcome_message,), daemon=True).start()
        
        # Iniciar interface visual
        try:
            self.interface.run()
        except KeyboardInterrupt:
            print("\n🤖 FHO Bot finalizado pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro na interface: {e}")
        finally:
            print("👋 Obrigado por usar o FHO Bot!")

if __name__ == "__main__":
    # Criar e executar bot visual aprimorado
    try:
        bot = FHOBotEnhanced()
        bot.run()
    except KeyboardInterrupt:
        print("\n🤖 Inicialização cancelada.")
    except Exception as e:
        print(f"\n❌ Erro ao inicializar: {e}")
        print("Verifique se todas as dependências estão instaladas.")
