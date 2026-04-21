#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure Cognitive Services Text-to-Speech
Implementação TTS usando vozes neurais de alta qualidade
"""

import azure.cognitiveservices.speech as speechsdk
import yaml
import os
import io
import tempfile
import time

# Suprimir mensagem pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class AzureTTS:
    def __init__(self, config_file="config.yaml"):
        """
        Inicializa Azure TTS
        
        Args:
            config_file: Caminho para arquivo de configuração
        """
        self.config = self._load_config(config_file)
        self.speech_config = None
        self.synthesizer = None
        
        # Inicializar pygame para reprodução de áudio
        try:
            import os
            os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
            pygame.mixer.init()
        except pygame.error as e:
            pass
        
        self._setup_azure()
    
    def _load_config(self, config_file):
        """Carrega configurações do arquivo YAML"""
        try:
            # Se config_file for caminho relativo, buscar no diretório pai
            if not os.path.isabs(config_file):
                config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_file)
            else:
                config_path = config_file
                
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            return {}
    
    def _setup_azure(self):
        """Configura Azure Speech Service"""
        try:
            azure_config = self.config.get('tts', {}).get('azure', {})
            
            api_key = azure_config.get('api_key', '')
            region = azure_config.get('regiao', 'eastus')
            
            if not api_key or api_key == "SUA_CHAVE_AZURE_AQUI":
                print("Azure TTS: ⚠️ Chave de API não configurada")
                print("Para obter uma chave gratuita:")
                print("1. Acesse: https://portal.azure.com")
                print("2. Crie um recurso 'Speech Services'")
                print("3. Copie a chave e cole no config.yaml")
                return False
            
            # Configurar Speech Service
            self.speech_config = speechsdk.SpeechConfig(
                subscription=api_key,
                region=region
            )
            
            # Configurar voz
            voice_name = azure_config.get('voz', 'pt-BR-FranciscaNeural')
            self.speech_config.speech_synthesis_voice_name = voice_name
            
            # Configurar formato de áudio
            self.speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
            )
            
            # Criar synthesizer
            self.synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=None  # Usar stream de áudio
            )
            
            return True
            
        except Exception as e:
            return False
    
    def is_available(self):
        """Verifica se Azure TTS está disponível"""
        return self.synthesizer is not None
    
    def get_ssml_text(self, text):
        """
        Gera SSML com configurações personalizadas
        
        Args:
            text: Texto para converter
            
        Returns:
            String SSML formatada
        """
        azure_config = self.config.get('tts', {}).get('azure', {})
        
        voice_name = azure_config.get('voz', 'pt-BR-FranciscaNeural')
        rate = azure_config.get('velocidade', '+0%')
        pitch = azure_config.get('pitch', '+0%')
        volume = azure_config.get('volume', '90%')
        
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="pt-BR">
            <voice name="{voice_name}">
                <prosody rate="{rate}" pitch="{pitch}" volume="{volume}">
                    {text}
                </prosody>
            </voice>
        </speak>
        """
        
        return ssml.strip()
    
    def speak(self, text):
        """
        Converte texto em fala usando Azure TTS
        
        Args:
            text: Texto para ser falado
        """
        if not self.is_available():
            return False
        
        if not text or not text.strip():
            return False
        
        try:
            # Gerar SSML
            ssml_text = self.get_ssml_text(text.strip())
            
            # Sintetizar
            result = self.synthesizer.speak_ssml_async(ssml_text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                # Reproduzir áudio
                self._play_audio(result.audio_data)
                return True
                
            elif result.reason == speechsdk.ResultReason.Canceled:
                return False
                
        except Exception as e:
            return False
    
    def _play_audio(self, audio_data):
        """
        Reproduz dados de áudio usando pygame
        
        Args:
            audio_data: Dados de áudio em bytes
        """
        try:
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            # Reproduzir com pygame
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Aguardar reprodução terminar
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Limpar arquivo temporário
            try:
                os.unlink(temp_path)
            except:
                pass
                
        except Exception as e:
            print(f"Azure TTS: ❌ Erro na reprodução: {e}")
    
    def list_available_voices(self):
        """Lista vozes neurais disponíveis para pt-BR"""
        voices = [
            {
                'name': 'pt-BR-FranciscaNeural',
                'gender': 'Feminina',
                'description': 'Voz feminina neural brasileira de alta qualidade'
            },
            {
                'name': 'pt-BR-AntonioNeural', 
                'gender': 'Masculina',
                'description': 'Voz masculina neural brasileira de alta qualidade'
            },
            {
                'name': 'pt-BR-BrendaNeural',
                'gender': 'Feminina', 
                'description': 'Voz feminina neural brasileira alternativa'
            }
        ]
        
        print("Azure TTS: Vozes disponíveis:")
        for voice in voices:
            print(f"  - {voice['name']} ({voice['gender']})")
            print(f"    {voice['description']}")
        
        return voices
    
    def test_voice(self, voice_name):
        """
        Testa uma voz específica
        
        Args:
            voice_name: Nome da voz para testar
        """
        if not self.is_available():
            print("Azure TTS: ❌ Serviço não disponível")
            return
        
        # Salvar voz atual
        original_voice = self.speech_config.speech_synthesis_voice_name
        
        try:
            # Configurar nova voz
            self.speech_config.speech_synthesis_voice_name = voice_name
            
            # Testar
            test_text = f"Olá! Esta é a voz {voice_name} falando em português do Brasil."
            self.speak(test_text)
            
        finally:
            # Restaurar voz original
            self.speech_config.speech_synthesis_voice_name = original_voice

# Função de conveniência
def create_azure_tts():
    """Cria instância do Azure TTS"""
    return AzureTTS()

if __name__ == "__main__":
    # Teste do módulo
    print("=== TESTE DO AZURE TTS ===")
    
    tts = AzureTTS()
    
    if tts.is_available():
        print("✅ Azure TTS configurado com sucesso!")
        
        # Listar vozes
        tts.list_available_voices()
        
        # Teste simples
        print("\nTestando voz padrão...")
        tts.speak("Olá! Este é um teste do Azure Text-to-Speech com qualidade neural.")
        
    else:
        print("❌ Azure TTS não está disponível")
        print("Verifique sua chave de API no config.yaml")
