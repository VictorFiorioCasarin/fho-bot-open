#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitário para trocar rapidamente entre Azure TTS e Windows SAPI
"""

import yaml
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from text_to_speech.tts_manager import TTSManager

def show_current_config():
    """Mostra configuração atual do TTS"""
    try:
        # Resolve the config path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "../config.yaml")
        
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        
        tts_config = config.get('tts', {})
        modo = tts_config.get('modo', 'sapi')
        
        print(f"🎤 CONFIGURAÇÃO ATUAL DO TTS")
        print("=" * 40)
        print(f"Modo ativo: {modo.upper()}")
        
        if modo == 'azure':
            azure_config = tts_config.get('azure', {})
            voz = azure_config.get('voz', 'Não configurada')
            regiao = azure_config.get('regiao', 'Não configurada')
            print(f"Voz Azure: {voz}")
            print(f"Região: {regiao}")
            print("💡 Qualidade: EXCELENTE (neural)")
            print("⚠️  Limite: 500k caracteres/mês")
        else:
            sapi_config = tts_config.get('sapi', {})
            tipo_voz = sapi_config.get('tipo_voz', 'auto')
            print(f"Voz SAPI: {tipo_voz}")
            print("💡 Qualidade: BÁSICA")
            print("✅ Limite: ILIMITADO")
        
        return config
        
    except Exception as e:
        print(f"❌ Erro ao ler configuração: {e}")
        return None

def switch_to_azure():
    """Muda para Azure TTS"""
    try:
        # Resolve the config path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "../config.yaml")
        
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        
        config['tts']['modo'] = 'azure'
        
        with open(config_path, "w", encoding="utf-8") as file:
            yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
        
        print("✅ Alternado para Azure TTS")
        print("🎯 Qualidade premium ativada!")
        
        # Testar
        tts = TTSManager()
        if tts.is_available():
            tts.speak("Azure TTS ativado! Qualidade neural superior!")
        
    except Exception as e:
        print(f"❌ Erro ao alternar para Azure: {e}")

def switch_to_sapi():
    """Muda para Windows SAPI"""
    try:
        # Resolve the config path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "../config.yaml")
        
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        
        config['tts']['modo'] = 'sapi'
        
        with open(config_path, "w", encoding="utf-8") as file:
            yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
        
        print("✅ Alternado para Windows SAPI")
        print("💰 Modo economia ativado!")
        
        # Testar
        tts = TTSManager()
        if tts.is_available():
            tts.speak("Windows SAPI ativado! Modo economia sem limites!")
        
    except Exception as e:
        print(f"❌ Erro ao alternar para SAPI: {e}")

def main():
    """Menu principal"""
    print("🔄 ALTERNADOR DE TTS - FHO BOT")
    print("=" * 40)
    
    while True:
        config = show_current_config()
        if not config:
            break
        
        print("\nOpções:")
        print("1. 🌐 Alternar para Azure TTS (qualidade premium)")
        print("2. 🖥️  Alternar para Windows SAPI (modo economia)")
        print("3. 🔊 Testar TTS atual")
        print("4. ℹ️  Mostrar informações detalhadas")
        print("5. ❌ Sair")
        
        choice = input("\nSua escolha (1-5): ").strip()
        
        if choice == "1":
            switch_to_azure()
        elif choice == "2":
            switch_to_sapi()
        elif choice == "3":
            tts = TTSManager()
            if tts.is_available():
                tts.test_current_tts()
            else:
                print("❌ TTS não disponível")
        elif choice == "4":
            show_detailed_info()
        elif choice == "5":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")
        print("\n" + "="*50 + "\n")

def show_detailed_info():
    """Mostra informações detalhadas sobre os provedores"""
    print("\n📊 COMPARAÇÃO DOS PROVEDORES TTS")
    print("=" * 50)
    
    print("\n🌐 AZURE TTS:")
    print("✅ Qualidade: EXCELENTE (vozes neurais)")
    print("✅ Vozes PT-BR: Francisca, Antonio, Brenda")
    print("✅ Naturalidade: Quase humana")
    print("✅ Expressividade: Alta")
    print("⚠️  Limite: 500.000 caracteres/mês")
    print("⚠️  Requer: Conexão com internet")
    print("💡 Ideal para: Demonstrações, apresentações")
    
    print("\n🖥️  WINDOWS SAPI:")
    print("✅ Disponibilidade: Sempre (offline)")
    print("✅ Limite: Ilimitado")
    print("✅ Velocidade: Instantânea")
    print("⚠️  Qualidade: Básica/robótica")
    print("⚠️  Vozes PT-BR: Apenas Maria")
    print("💡 Ideal para: Testes, desenvolvimento")
    
    print("\n🎯 RECOMENDAÇÕES:")
    print("- Use Azure para demonstrações importantes")
    print("- Use SAPI para desenvolvimento e testes")
    print("- Monitore uso do Azure para não exceder limite")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Comando via linha de comando
        comando = sys.argv[1].lower()
        
        if comando == "azure":
            switch_to_azure()
        elif comando == "sapi":
            switch_to_sapi()
        elif comando == "status":
            show_current_config()
        else:
            print("Uso: python switch_tts.py [azure|sapi|status]")
    else:
        # Menu interativo
        main()
