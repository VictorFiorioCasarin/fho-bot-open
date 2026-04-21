#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guia para obter chave gratuita do Azure Speech Services
"""

import webbrowser
import time

def show_azure_setup_guide():
    """Mostra guia completo para configurar Azure TTS"""
    
    print("""
🌐 GUIA: CONFIGURAR AZURE TEXT-TO-SPEECH (GRATUITO)
===================================================

BENEFÍCIOS DO AZURE TTS:
✅ Qualidade de voz EXCELENTE (neural/quase humana)
✅ Vozes PT-BR: Francisca, Antonio, Brenda
✅ 500.000 caracteres GRATUITOS por mês
✅ Sem necessidade de cartão de crédito (trial)
✅ Latência baixa, muito confiável

PASSO 1: CRIAR CONTA AZURE (GRATUITA)
=====================================
""")
    
    input("Pressione ENTER para abrir Azure Portal...")
    webbrowser.open("https://portal.azure.com")
    
    print("""
No Azure Portal:
1. Clique em "Criar uma conta gratuita" (se não tiver)
2. Ou faça login com conta Microsoft existente
3. Não precisa de cartão de crédito para Speech Services

PASSO 2: CRIAR RECURSO SPEECH SERVICES
=======================================
""")
    
    input("Pressione ENTER para abrir página de criação...")
    webbrowser.open("https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices")
    
    print("""
Na página de criação:
1. Subscription: Selecione sua subscription
2. Resource Group: Crie novo (ex: "fho-bot-rg")
3. Region: Escolha "East US" ou "Brazil South"
4. Name: Nome único (ex: "fho-bot-speech-service")
5. Pricing Tier: Selecione "Free F0" (500k chars/mês grátis)
6. Clique "Review + Create" e depois "Create"

PASSO 3: OBTER CHAVES DE API
============================
""")
    
    input("Pressione ENTER quando recurso estiver criado...")
    
    print("""
Após criar o recurso:
1. Vá para o recurso criado
2. No menu esquerdo, clique "Keys and Endpoint"
3. Copie "KEY 1" (algo como: 1234567890abcdef...)
4. Anote também a "REGION" (ex: eastus, brazilsouth)

PASSO 4: CONFIGURAR NO SEU BOT
==============================
""")
    
    api_key = input("Cole aqui sua KEY 1 do Azure: ").strip()
    region = input("Digite sua REGION (ex: eastus): ").strip() or "eastus"
    
    if api_key and api_key != "SUA_CHAVE_AZURE_AQUI":
        # Atualizar config.yaml
        try:
            import yaml
            import os
            
            # Resolve the config path relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, "../config.yaml")
            
            with open(config_path, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
            
            # Atualizar configurações
            config['tts']['azure']['api_key'] = api_key
            config['tts']['azure']['regiao'] = region
            config['tts']['modo'] = 'azure'  # Ativar Azure como padrão
            
            with open(config_path, "w", encoding="utf-8") as file:
                yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
            
            print(f"""
✅ CONFIGURAÇÃO SALVA COM SUCESSO!
=================================

Configurações aplicadas:
- API Key: {api_key[:8]}...
- Região: {region}
- Modo TTS: Azure (ativado)

Agora execute: python main.py
Você vai ouvir a diferença de qualidade!
""")
            
        except Exception as e:
            print(f"""
❌ Erro ao salvar configuração: {e}

Configure manualmente no config.yaml:
tts:
  modo: azure
  azure:
    api_key: "{api_key}"
    regiao: "{region}"
""")
    else:
        print("""
⚠️ Chave não fornecida. Configure manualmente no config.yaml:

tts:
  modo: azure
  azure:
    api_key: "SUA_CHAVE_AQUI"
    regiao: "eastus"
""")

def test_azure_configuration():
    """Testa se Azure está configurado corretamente"""
    try:
        from azure_tts import AzureTTS
        
        print("\n🧪 TESTANDO CONFIGURAÇÃO AZURE...")
        
        tts = AzureTTS()
        
        if tts.is_available():
            print("✅ Azure TTS configurado corretamente!")
            print("Testando síntese de voz...")
            
            test_text = "Parabéns! O Azure Text-to-Speech está funcionando perfeitamente!"
            success = tts.speak(test_text)
            
            if success:
                print("✅ Teste de voz concluído com sucesso!")
                print("Agora você pode usar vozes neurais de alta qualidade!")
            else:
                print("❌ Erro no teste de voz")
        else:
            print("❌ Azure TTS não está disponível")
            print("Verifique sua chave de API e conexão com internet")
            
    except ImportError:
        print("❌ Módulo azure_tts não encontrado")
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

def main():
    """Função principal"""
    print("🎤 CONFIGURADOR AZURE TTS PARA FHO BOT")
    print("=" * 50)
    
    while True:
        print("""
Escolha uma opção:
1. 📋 Mostrar guia completo de configuração
2. 🧪 Testar configuração atual
3. 🌐 Abrir Azure Portal diretamente
4. 📖 Mostrar vozes disponíveis
5. ❌ Sair
""")
        
        choice = input("Sua escolha (1-5): ").strip()
        
        if choice == "1":
            show_azure_setup_guide()
        elif choice == "2":
            test_azure_configuration()
        elif choice == "3":
            webbrowser.open("https://portal.azure.com")
            print("Azure Portal aberto no navegador!")
        elif choice == "4":
            print("""
🎭 VOZES NEURAIS DISPONÍVEIS (PT-BR):

1. pt-BR-FranciscaNeural (Feminina)
   - Voz natural e expressiva
   - Ideal para assistentes virtuais
   - Padrão recomendado

2. pt-BR-AntonioNeural (Masculina)  
   - Voz masculina profissional
   - Tom amigável e claro
   - Ótima para narrações

3. pt-BR-BrendaNeural (Feminina)
   - Voz alternativa feminina
   - Tom mais jovem
   - Para diversidade de personagens
""")
        elif choice == "5":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()
