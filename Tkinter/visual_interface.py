#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Vi        self.faces = {
            BotState.IDLE: "😊",
            BotState.LISTENING: "👂",
            BotState.THINKING: "🤔",
            BotState.SPEAKING: "😀"
        }o FHO Bot
Janela Tkinter com indicadores visuais de estado e personagem ASCII
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from enum import Enum
from typing import Callable, Optional

class BotState(Enum):
    """Estados visuais do bot"""
    IDLE = "idle"          # 😊 Neutro - Aguardando
    LISTENING = "listening" # 🟢 Verde - Escutando (STT)
    THINKING = "thinking"   # 🟠 Laranja - Processando (LLM)
    SPEAKING = "speaking"   # 🔵 Azul - Falando (TTS)

class VisualInterface:
    """Interface visual do FHO Bot com estados e animações"""
    
    def __init__(self, on_text_input: Optional[Callable] = None, on_voice_input: Optional[Callable] = None):
        """
        Inicializa a interface visual
        
        Args:
            on_text_input: Callback para entrada de texto
            on_voice_input: Callback para entrada de voz
        """
        self.on_text_input = on_text_input
        self.on_voice_input = on_voice_input
        
        # Estado atual
        self.current_state = BotState.IDLE
        self.animation_running = False
        
        # Criar janela principal
        self.root = tk.Tk()
        self.root.title("FHO Bot - Assistente de Engenharia de Computação")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        
        # Impedir redimensionamento
        self.root.resizable(False, False)
        
        # Configurar estilo
        self.setup_styles()
        
        # Criar interface
        self.create_interface()
        
        # Iniciar no estado neutro
        self.set_state(BotState.IDLE)
    
    def setup_styles(self):
        """Configura os estilos da interface"""
        self.colors = {
            BotState.IDLE: "#3498db",      # Azul neutro
            BotState.LISTENING: "#2ecc71", # Verde - escutando
            BotState.THINKING: "#f39c12",  # Laranja - pensando
            BotState.SPEAKING: "#3498db"   # Azul - falando
        }
        
        self.faces = {
            BotState.IDLE: "😊",
            BotState.LISTENING: "👂",
            BotState.THINKING: "🤔",
            BotState.SPEAKING: "😀"
        }
    
    def create_interface(self):
        """Cria todos os elementos da interface"""
        # Frame principal do personagem
        self.character_frame = tk.Frame(self.root, bg='#2c3e50')
        self.character_frame.pack(pady=20)
        
        # Status do bot (cor de fundo)
        self.status_frame = tk.Frame(self.character_frame, bg=self.colors[BotState.IDLE], 
                                   width=300, height=200, relief='ridge', bd=3)
        self.status_frame.pack_propagate(False)
        self.status_frame.pack()
        
        # ASCII Art do rosto
        self.face_label = tk.Label(self.status_frame, text=self.faces[BotState.IDLE], 
                                 font=('Arial', 48), bg=self.colors[BotState.IDLE], fg='white')
        self.face_label.pack(expand=True)
        
        # Estado atual em texto
        self.state_label = tk.Label(self.character_frame, text="Aguardando...", 
                                  font=('Arial', 12, 'bold'), bg='#2c3e50', fg='white')
        self.state_label.pack(pady=(10, 0))
        
        # Frame de controles
        self.controls_frame = tk.Frame(self.root, bg='#2c3e50')
        self.controls_frame.pack(pady=20)
        
        # Botões de ação
        self.voice_button = tk.Button(self.controls_frame, text="🎤 Falar", 
                                    font=('Arial', 12, 'bold'), bg='#27ae60', fg='white',
                                    command=self.on_voice_button_click, width=12)
        self.voice_button.pack(side=tk.LEFT, padx=10)
        
        # Frame de entrada de texto
        self.text_frame = tk.Frame(self.root, bg='#2c3e50')
        self.text_frame.pack(pady=10, padx=20, fill='x')
        
        # Campo de entrada de texto
        self.text_entry = tk.Entry(self.text_frame, font=('Arial', 12), width=40)
        self.text_entry.pack(side=tk.LEFT, padx=(0, 10), fill='x', expand=True)
        self.text_entry.bind('<Return>', self.on_text_entry_return)
        
        # Botão enviar
        self.send_button = tk.Button(self.text_frame, text="Enviar", 
                                   font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                                   command=self.on_send_button_click)
        self.send_button.pack(side=tk.RIGHT)
        
        # Área de conversação
        self.conversation_frame = tk.Frame(self.root, bg='#2c3e50')
        self.conversation_frame.pack(pady=(10, 20), padx=20, fill='both', expand=True)
        
        # Área de texto scrollável para conversação
        self.conversation_text = scrolledtext.ScrolledText(
            self.conversation_frame, 
            font=('Arial', 11),
            bg='#34495e',
            fg='white',
            insertbackground='white',
            wrap=tk.WORD,
            height=8,
            state=tk.DISABLED
        )
        self.conversation_text.pack(fill='both', expand=True)
        
        # Configurar tags para diferentes tipos de mensagem
        self.conversation_text.tag_configure("user", foreground="#3498db")
        self.conversation_text.tag_configure("bot", foreground="#2ecc71")
        self.conversation_text.tag_configure("system", foreground="#f39c12")
    
    def set_state(self, state: BotState):
        """
        Muda o estado visual do bot
        
        Args:
            state: Novo estado do bot
        """
        self.current_state = state
        
        # Atualizar cor de fundo
        color = self.colors[state]
        self.status_frame.configure(bg=color)
        self.face_label.configure(bg=color)
        
        # Atualizar emoji
        self.face_label.configure(text=self.faces[state])
        
        # Atualizar texto do estado
        state_texts = {
            BotState.IDLE: "Aguardando...",
            BotState.LISTENING: "Escutando você... 👂",
            BotState.THINKING: "Processando... 🤔",
            BotState.SPEAKING: "Falando... 😀"
        }
        self.state_label.configure(text=state_texts[state])
        
        # Iniciar animação se necessário
        if state in [BotState.LISTENING, BotState.THINKING, BotState.SPEAKING]:
            self.start_pulse_animation()
        else:
            self.stop_animation()
    
    def start_pulse_animation(self):
        """Inicia animação de pulso para estados ativos"""
        if not self.animation_running:
            self.animation_running = True
            self.pulse_animation()
    
    def stop_animation(self):
        """Para a animação"""
        self.animation_running = False
    
    def pulse_animation(self):
        """Animação de pulso do personagem"""
        if not self.animation_running:
            return
        
        # Efeito de pulso mudando o tamanho da fonte
        current_size = int(self.face_label.cget('font').split()[1])
        if current_size >= 48:
            new_size = 44
        else:
            new_size = 48
            
        self.face_label.configure(font=('Arial', new_size))
        
        # Agendar próximo frame da animação
        self.root.after(800, self.pulse_animation)
    
    def add_message(self, sender: str, message: str):
        """
        Adiciona mensagem à área de conversação
        
        Args:
            sender: "user", "bot", ou "system"
            message: Texto da mensagem
        """
        self.conversation_text.configure(state=tk.NORMAL)
        
        # Adicionar timestamp
        timestamp = time.strftime("%H:%M:%S")
        
        if sender == "user":
            self.conversation_text.insert(tk.END, f"[{timestamp}] Você: ", "user")
        elif sender == "bot":
            self.conversation_text.insert(tk.END, f"[{timestamp}] FHO Bot: ", "bot")
        else:
            self.conversation_text.insert(tk.END, f"[{timestamp}] ", "system")
        
        self.conversation_text.insert(tk.END, f"{message}\n\n")
        
        # Scroll para o final
        self.conversation_text.see(tk.END)
        self.conversation_text.configure(state=tk.DISABLED)
    
    def on_voice_button_click(self):
        """Callback para botão de voz"""
        if self.on_voice_input:
            # Executar em thread separada para não bloquear a UI
            threading.Thread(target=self.on_voice_input, daemon=True).start()
    
    def on_text_entry_return(self, event):
        """Callback para Enter no campo de texto"""
        self.on_send_button_click()
    
    def on_send_button_click(self):
        """Callback para botão enviar"""
        text = self.text_entry.get().strip()
        if text and self.on_text_input:
            self.text_entry.delete(0, tk.END)
            # Executar em thread separada para não bloquear a UI
            threading.Thread(target=self.on_text_input, args=(text,), daemon=True).start()
    
    def show_welcome_message(self):
        """Mostra mensagem de boas-vindas"""
        welcome = "Olá! Eu sou seu assistente. Estou aqui para conversar com você sobre o curso de Engenharia de Computação da FHO!"
        self.add_message("bot", welcome)
        self.add_message("system", "Digite sua mensagem ou clique em 'Falar' para usar voz.")
    
    def run(self):
        """Inicia a interface visual"""
        self.show_welcome_message()
        self.root.mainloop()
    
    def close(self):
        """Fecha a interface"""
        self.root.quit()
        self.root.destroy()

# Função de teste da interface
if __name__ == "__main__":
    def test_text_input(text):
        """Teste para entrada de texto"""
        interface.add_message("user", text)
        interface.set_state(BotState.THINKING)
        time.sleep(2)  # Simular processamento
        interface.add_message("bot", f"Você disse: {text}")
        interface.set_state(BotState.IDLE)
    
    def test_voice_input():
        """Teste para entrada de voz"""
        interface.set_state(BotState.LISTENING)
        time.sleep(2)  # Simular escuta
        interface.add_message("user", "[Mensagem de voz]")
        interface.set_state(BotState.THINKING)
        time.sleep(2)  # Simular processamento
        interface.set_state(BotState.SPEAKING)
        interface.add_message("bot", "Entendi sua mensagem de voz!")
        time.sleep(2)  # Simular fala
        interface.set_state(BotState.IDLE)
    
    # Criar e executar interface de teste
    interface = VisualInterface(on_text_input=test_text_input, on_voice_input=test_voice_input)
    interface.run()
