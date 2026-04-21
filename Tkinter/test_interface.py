#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Simples da Interface Visual
Teste básico sem dependências do RAG
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_visual import EnhancedVisualInterface, BotState

def simple_response(text: str):
    """Resposta simples para teste"""
    return f"Você disse: '{text}'. Esta é uma resposta de teste do FHO Bot!"

def main():
    """Função principal do teste"""
    
    def handle_text_input(text: str):
        """Processa entrada de texto"""
        # Adicionar mensagem do usuário
        interface.add_message("user", text)
        
        # Simular pensamento
        interface.set_state(BotState.THINKING)
        
        # Gerar resposta simples
        response = simple_response(text)
        
        # Mostrar falando
        interface.set_state(BotState.SPEAKING)
        interface.add_message("bot", response)
        
        # Voltar ao estado idle
        interface.set_state(BotState.IDLE)
    
    def handle_voice_input():
        """Processa entrada de voz (simulado)"""
        interface.add_message("user", "Entrada de voz simulada")
        handle_text_input("Esta é uma entrada de voz simulada")
    
    # Criar interface
    interface = EnhancedVisualInterface(
        on_text_input=handle_text_input,
        on_voice_input=handle_voice_input
    )
    
    # Atualizar status
    interface.update_tts_status("Modo Teste - Interface Reorganizada ✅")
    
    # Executar
    interface.run()

if __name__ == "__main__":
    main()
