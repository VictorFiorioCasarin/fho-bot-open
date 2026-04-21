#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo das Funcionalidades Visuais do FHO Bot
Script para demonstrar todos os estados visuais e animações
"""

import time
import threading
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_visual import EnhancedVisualInterface, BotState

class BotDemo:
    """Demonstração das funcionalidades visuais"""
    
    def __init__(self):
        """Inicializa a demonstração"""
        self.interface = EnhancedVisualInterface(
            on_text_input=self.demo_text_input,
            on_voice_input=self.demo_voice_input
        )
        
        # Atualizar status inicial
        self.interface.update_tts_status("Demo Mode - Todas as funcionalidades")
    
    def demo_text_input(self, text: str):
        """Demonstra processamento de entrada de texto"""
        # Adicionar mensagem do usuário
        self.interface.add_message("user", text)
        
        # Simular estados do bot
        self.simulate_bot_processing(text)
    
    def demo_voice_input(self):
        """Demonstra processamento de entrada de voz"""
        # Estado: Escutando
        self.interface.set_state(BotState.LISTENING)
        self.interface.add_message("system", "🎤 Simulando captura de voz...")
        
        # Simular escuta
        time.sleep(3)
        
        # Adicionar "mensagem de voz"
        demo_voice_text = "Como funciona o curso de Engenharia de Computação?"
        self.interface.add_message("user", f"🎤 \"{demo_voice_text}\"")
        
        # Simular processamento
        self.simulate_bot_processing(demo_voice_text)
    
    def simulate_bot_processing(self, user_input: str):
        """
        Simula o processamento completo do bot
        
        Args:
            user_input: Entrada do usuário
        """
        # Estado: Pensando
        self.interface.set_state(BotState.THINKING)
        self.interface.add_message("system", "🧠 Processando com IA...")
        
        # Simular tempo de processamento
        time.sleep(3)
        
        # Gerar resposta demo baseada na entrada
        response = self.generate_demo_response(user_input)
        
        # Estado: Falando
        self.interface.set_state(BotState.SPEAKING)
        self.interface.add_message("bot", response)
        self.interface.add_message("system", "🔊 Reproduzindo resposta por voz...")
        
        # Simular tempo de fala
        time.sleep(4)
        
        # Voltar ao estado neutro
        self.interface.set_state(BotState.IDLE)
        self.interface.add_message("system", "✅ Pronto para próxima pergunta!")
    
    def generate_demo_response(self, user_input: str) -> str:
        """
        Gera resposta de demonstração baseada na entrada
        
        Args:
            user_input: Entrada do usuário
            
        Returns:
            str: Resposta de demonstração
        """
        # Respostas demo baseadas em palavras-chave
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['curso', 'engenharia', 'computação']):
            return ("O curso de Engenharia de Computação da FHO é fantástico! "
                   "Você aprende programação, eletrônica, matemática e muito mais. "
                   "É um curso que prepara profissionais completos para o mercado de tecnologia.")
        
        elif any(word in user_lower for word in ['mercado', 'trabalho', 'carreira']):
            return ("O mercado para Engenheiros de Computação está em alta! "
                   "Você pode trabalhar com desenvolvimento de software, hardware, "
                   "IoT, inteligência artificial, sistemas embarcados e muito mais!")
        
        elif any(word in user_lower for word in ['disciplinas', 'matérias', 'grade']):
            return ("As disciplinas incluem Programação, Circuitos Digitais, "
                   "Estruturas de Dados, Sistemas Operacionais, Redes, "
                   "Inteligência Artificial, Banco de Dados e muito mais!")
        
        elif any(word in user_lower for word in ['fho', 'faculdade', 'instituição']):
            return ("A FHO é uma instituição de excelência! "
                   "Temos laboratórios modernos, professores qualificados "
                   "e uma metodologia de ensino inovadora que prepara "
                   "nossos alunos para serem protagonistas no mercado!")
        
        else:
            return ("Excelente pergunta! O curso de Engenharia de Computação da FHO "
                   "oferece uma formação completa e inovadora. "
                   "Que tal perguntar algo mais específico sobre o curso?")
    
    def auto_demo(self):
        """Executa demonstração automática"""
        def demo_sequence():
            # Aguardar interface carregar
            time.sleep(2)
            
            # Sequência de demonstração
            demo_messages = [
                "O que é Engenharia de Computação?",
                "Como está o mercado de trabalho?",
                "Quais são as principais disciplinas?",
                "Por que escolher a FHO?"
            ]
            
            for i, message in enumerate(demo_messages):
                self.interface.add_message("system", f"🎬 Demo {i+1}/4: Simulando pergunta...")
                time.sleep(1)
                
                # Simular entrada do usuário
                self.demo_text_input(message)
                
                # Aguardar finalizar processamento
                time.sleep(8)
            
            # Finalizar demo
            self.interface.add_message("system", "🎉 Demonstração concluída! Agora você pode interagir livremente.")
        
        # Executar demo em thread separada
        threading.Thread(target=demo_sequence, daemon=True).start()
    
    def run(self, auto_start=False):
        """
        Executa a demonstração
        
        Args:
            auto_start: Se True, inicia demo automática
        """
        # Mostrar mensagem de boas-vindas personalizada
        self.interface.add_message("bot", 
            "🎬 Bem-vindo à DEMONSTRAÇÃO do FHO Bot! "
            "Esta é uma versão de apresentação que simula todas as funcionalidades visuais.")
        
        self.interface.add_message("system", 
            "💡 Funcionalidades disponíveis:\n"
            "• 😊 Estados visuais com cores e animações\n"
            "• 🎤 Simulação de entrada por voz\n"
            "• 🧠 Visualização do processamento da IA\n"
            "• 🗣️ Indicação visual durante resposta\n"
            "• ⚙️ Interface moderna e intuitiva")
        
        if auto_start:
            self.interface.add_message("system", "🚀 Iniciando demonstração automática em 3 segundos...")
            self.auto_demo()
        
        # Iniciar interface
        self.interface.run()

if __name__ == "__main__":
    print("🎬 FHO Bot - Demonstração Visual")
    print("=" * 50)
    print("Esta demonstração mostra todas as funcionalidades visuais:")
    print("• Estados com cores (Verde, Laranja, Azul)")
    print("• Animações de pulso")
    print("• Simulação de STT e TTS")
    print("• Interface moderna com Tkinter")
    print("=" * 50)
    
    # Perguntar se quer demo automática
    choice = input("Deseja executar demo automática? (s/n): ").lower().strip()
    auto_start = choice in ['s', 'sim', 'y', 'yes']
    
    # Criar e executar demo
    demo = BotDemo()
    demo.run(auto_start=auto_start)
