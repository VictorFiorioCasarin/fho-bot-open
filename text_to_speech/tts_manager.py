#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS Manager - Gerencia diferentes provedores de Text-to-Speech
Suporta Windows SAPI e Azure Cognitive Services
"""

import yaml
import os
from .windows_sapi_tts import WindowsSAPITTS
from .azure_tts import AzureTTS

class TTSManager:
    def __init__(self, config_file="config.yaml"):
        """
        Inicializa o gerenciador de TTS
        
        Args:
            config_file: Caminho para arquivo de configuração
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.current_tts = None
        
        self._initialize_tts()
    
    def _load_config(self):
        """Carrega configurações do arquivo YAML"""
        try:
            # Se config_file for caminho relativo, buscar no diretório pai
            if not os.path.isabs(self.config_file):
                config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.config_file)
            else:
                config_path = self.config_file
                
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"TTS Manager: ❌ Erro ao carregar config: {e}")
            return {}
    
    def _initialize_tts(self):
        """Inicializa o provedor de TTS baseado na configuração"""
        tts_config = self.config.get('tts', {})
        
        if not tts_config.get('habilitado', True):
            return
        
        modo = tts_config.get('modo', 'sapi').lower()
        
        if modo == 'azure':
            self.current_tts = AzureTTS()
            
            if not self.current_tts.is_available():
                # Fallback silencioso para SAPI
                self.current_tts = WindowsSAPITTS()
                
        elif modo == 'sapi':
            self.current_tts = WindowsSAPITTS()
            
        else:
            # Modo não reconhecido, usar SAPI como padrão
            self.current_tts = WindowsSAPITTS()
    
    def speak(self, text):
        """
        Converte texto em fala usando o provedor ativo
        
        Args:
            text: Texto para ser falado
        """
        if not self.current_tts:
            return False
        
        if not text or not text.strip():
            return False
        
        try:
            return self.current_tts.speak(text)
        except Exception as e:
            return False
    
    def is_available(self):
        """Verifica se TTS está disponível"""
        return self.current_tts is not None
    
    def get_simple_info(self):
        """Retorna informação simples sobre o TTS para o usuário"""
        if not self.current_tts:
            return "Desabilitado"
        
        tts_config = self.config.get('tts', {})
        modo = tts_config.get('modo', 'sapi').lower()
        
        if isinstance(self.current_tts, AzureTTS):
            azure_config = tts_config.get('azure', {})
            voice = azure_config.get('voz', 'pt-BR-FranciscaNeural')
            if 'Francisca' in voice or 'Brenda' in voice:
                gender = "Feminina"
            elif 'Antonio' in voice:
                gender = "Masculina"
            else:
                gender = "Neural"
            return f"Azure - {gender}"
            
        elif isinstance(self.current_tts, WindowsSAPITTS):
            sapi_config = tts_config.get('sapi', {})
            voice_pref = sapi_config.get('tipo_voz', 'auto')
            if voice_pref.lower() == 'feminina':
                gender = "Feminina"
            elif voice_pref.lower() == 'masculina':
                gender = "Masculina"
            else:
                gender = "Padrão"
            return f"Windows SAPI - {gender}"
        
    def get_current_provider(self):
        """Retorna o nome do provedor atual"""
        if isinstance(self.current_tts, AzureTTS):
            return "Azure TTS"
        elif isinstance(self.current_tts, WindowsSAPITTS):
            return "Windows SAPI"
        else:
            return "Nenhum"
    
    def get_tts_info(self):
        """Retorna informações sobre o TTS atual"""
        if not self.current_tts:
            return "TTS não disponível"
        
        provider = self.get_current_provider()
        tts_config = self.config.get('tts', {})
        
        if isinstance(self.current_tts, AzureTTS):
            azure_config = tts_config.get('azure', {})
            voice = azure_config.get('voz', 'pt-BR-FranciscaNeural')
            region = azure_config.get('regiao', 'eastus')
            return f"{provider} - Voz: {voice} (Região: {region})"
            
        elif isinstance(self.current_tts, WindowsSAPITTS):
            sapi_config = tts_config.get('sapi', {})
            voice = sapi_config.get('tipo_voz', 'auto')
            return f"{provider} - Preferência: {voice}"
        
        return provider
    
    def list_available_voices(self):
        """Lista vozes disponíveis do provedor atual"""
        if not self.current_tts:
            print("TTS Manager: ❌ Nenhum provedor ativo")
            return []
        
        if hasattr(self.current_tts, 'list_available_voices'):
            return self.current_tts.list_available_voices()
        else:
            print("TTS Manager: ⚠️ Provedor não suporta listagem de vozes")
            return []
    
    def switch_provider(self, new_mode):
        """
        Altera o provedor de TTS
        
        Args:
            new_mode: 'azure' ou 'sapi'
        """
        print(f"TTS Manager: 🔄 Alternando para {new_mode}...")
        
        # Atualizar configuração
        if 'tts' not in self.config:
            self.config['tts'] = {}
        self.config['tts']['modo'] = new_mode
        
        # Salvar configuração
        try:
            with open(self.config_file, 'w', encoding='utf-8') as file:
                yaml.dump(self.config, file, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"TTS Manager: ❌ Erro ao salvar config: {e}")
        
        # Reinicializar
        self._initialize_tts()
    
    def quick_switch_to_sapi(self):
        """Muda rapidamente para Windows SAPI (para economizar Azure)"""
        print("TTS Manager: 🔄 Alternando para Windows SAPI (modo economia)")
        self.switch_provider('sapi')
    
    def quick_switch_to_azure(self):
        """Muda rapidamente para Azure TTS (para qualidade premium)"""
        print("TTS Manager: 🔄 Alternando para Azure TTS (modo qualidade)")
        self.switch_provider('azure')
    
    def test_current_tts(self):
        """Testa o TTS atual"""
        if not self.is_available():
            print("TTS Manager: ❌ TTS não disponível para teste")
            return False
        
        provider = self.get_current_provider()
        test_text = f"Testando {provider}. A qualidade da voz está excelente!"
        
        print(f"TTS Manager: 🔊 Testando {provider}...")
        return self.speak(test_text)

# Função de conveniência para criar instância global
_tts_manager_instance = None

def get_tts_manager():
    """Retorna instância singleton do TTS Manager"""
    global _tts_manager_instance
    if _tts_manager_instance is None:
        _tts_manager_instance = TTSManager()
    return _tts_manager_instance

if __name__ == "__main__":
    # Teste do TTS Manager
    print("=== TESTE DO TTS MANAGER ===")
    
    manager = TTSManager()
    
    print(f"Provedor atual: {manager.get_tts_info()}")
    print()
    
    if manager.is_available():
        # Testar provedor atual
        manager.test_current_tts()
        
        # Listar vozes se disponível
        print("\nListando vozes disponíveis...")
        manager.list_available_voices()
        
    else:
        print("❌ TTS não está disponível")
        print("Verifique sua configuração no config.yaml")
