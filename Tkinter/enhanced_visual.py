#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Visual Aprimora             self.faces = {
            BotState.IDLE: "😊",
            BotState.LISTENING: "👂",
            BotState.THINKING: "🤔",
            BotState.SPEAKING: "😀"
        }f.faces = {
            BotState.IDLE: "😊",
            BotState.LISTENING: "👂",
            BotState.THINKING: "🤔",
            BotState.SPEAKING: "😀"
        }FHO Bot
Versão com mais recursos visuais e melhor UX
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from enum import Enum
from typing import Callable, Optional
from datetime import datetime

class BotState(Enum):
    """Estados visuais do bot"""
    IDLE = "idle"          # 😊 Neutro - Aguardando
    LISTENING = "listening" # 🟢 Verde - Escutando (STT)
    THINKING = "thinking"   # 🟠 Laranja - Processando (LLM)
    SPEAKING = "speaking"   # 🔵 Azul - Falando (TTS)

class EnhancedVisualInterface:
    """Interface visual aprimorada do FHO Bot"""
    
    def __init__(self, on_text_input: Optional[Callable] = None, on_voice_input: Optional[Callable] = None):
        """
        Inicializa a interface visual aprimorada
        
        Args:
            on_text_input: Callback para entrada de texto
            on_voice_input: Callback para entrada de voz
        """
        self.on_text_input = on_text_input
        self.on_voice_input = on_voice_input
        
        # Estado atual
        self.current_state = BotState.IDLE
        self.animation_running = False
        
        # Controle de tamanho do personagem (True = grande/500, False = médio/300)
        self.large_character = True
        self.pulse_max = 500
        self.pulse_min = 495
        
        # Criar janela principal
        self.root = tk.Tk()
        self.root.title("🤖 FHO Bot - Assistente de Engenharia de Computação")
        
        # Configurar tela cheia
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#1a1a1a')
        
        # Adicionar bind para sair da tela cheia com Escape
        self.root.bind('<Escape>', lambda e: self.toggle_fullscreen())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        
        # Centralizar janela
        self.center_window()
        
        # Configurar estilo
        self.setup_styles()
        
        # Criar interface
        self.create_interface()
        
        # Iniciar no estado neutro
        self.set_state(BotState.IDLE)
        
        # Atualizar botão de tela cheia (já que inicia em fullscreen)
        if hasattr(self, 'fullscreen_button'):
            self.fullscreen_button.config(text="◱ Sair Tela Cheia")
        
        # Atualizar botão de tamanho (já que inicia em tamanho grande)
        if hasattr(self, 'character_size_button'):
            self.character_size_button.config(text="📏 Tamanho Grande")
        
        # Configurar eventos de teclado
        self.setup_keyboard_shortcuts()
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def toggle_fullscreen(self):
        """Alterna entre tela cheia e janela normal"""
        current_state = self.root.attributes('-fullscreen')
        if current_state:
            # Sair da tela cheia
            self.root.attributes('-fullscreen', False)
            self.root.geometry("800x700")  # Tamanho maior que o original
            self.center_window()
            # Atualizar texto do botão
            if hasattr(self, 'fullscreen_button'):
                self.fullscreen_button.config(text="⛶ Tela Cheia")
        else:
            # Entrar em tela cheia
            self.root.attributes('-fullscreen', True)
            # Atualizar texto do botão
            if hasattr(self, 'fullscreen_button'):
                self.fullscreen_button.config(text="◱ Sair Tela Cheia")
    
    def toggle_character_size(self):
        """Alterna o tamanho do personagem entre grande (500) e médio (300)"""
        if self.large_character:
            # Mudar para tamanho médio
            new_size = 300
            new_frame_size = 400
            new_pulse_max = 300
            new_pulse_min = 295
            button_text = "📏 Tamanho Médio"
            self.large_character = False
        else:
            # Mudar para tamanho grande
            new_size = 500
            new_frame_size = 650
            new_pulse_max = 500
            new_pulse_min = 495
            button_text = "📏 Tamanho Grande"
            self.large_character = True
        
        # Atualizar o emoji
        self.face_label.configure(font=('Arial', new_size))
        
        # Atualizar o frame do avatar
        self.avatar_frame.configure(width=new_frame_size, height=new_frame_size)
        
        # Atualizar texto do botão
        if hasattr(self, 'character_size_button'):
            self.character_size_button.config(text=button_text)
        
        # Armazenar novos valores de pulso para animação
        self.pulse_max = new_pulse_max
        self.pulse_min = new_pulse_min
    
    def setup_styles(self):
        """Configura os estilos da interface"""
        self.colors = {
            BotState.IDLE: "#2c3e50",      # Azul escuro neutro
            BotState.LISTENING: "#27ae60", # Verde - escutando
            BotState.THINKING: "#f39c12",  # Laranja - pensando
            BotState.SPEAKING: "#3498db"   # Azul claro - falando
        }
        
        self.faces = {
            BotState.IDLE: "😊",
            BotState.LISTENING: "👂",
            BotState.THINKING: "🤔",
            BotState.SPEAKING: "😀"
        }
        
        self.state_descriptions = {
            BotState.IDLE: "Aguardando sua mensagem...",
            BotState.LISTENING: "Escutando você... 🎤",
            BotState.THINKING: "Processando resposta... 🧠",
            BotState.SPEAKING: "Respondendo... 🔊"
        }
    
    def setup_keyboard_shortcuts(self):
        """Configura atalhos de teclado"""
        self.root.bind('<Control-Return>', lambda e: self.on_voice_button_click())
        self.root.bind('<F1>', lambda e: self.show_help())
        # Escape agora alterna tela cheia, Ctrl+Q para sair
        self.root.bind('<Control-q>', lambda e: self.on_exit())
        self.root.bind('<Alt-F4>', lambda e: self.on_exit())
    
    def create_interface(self):
        """Cria todos os elementos da interface"""
        # Header com título
        self.create_header()
        
        # Frame principal do personagem
        self.create_character_area()
        
        # Frame de controles
        self.create_controls()
        
        # Frame de entrada de texto
        self.create_text_input()
        
        # Área de conversação
        self.create_conversation_area()
        
        # Status bar
        self.create_status_bar()
    
    def create_header(self):
        """Cria o cabeçalho da aplicação"""
        header_frame = tk.Frame(self.root, bg='#1a1a1a', height=50)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Logo e título
        title_label = tk.Label(header_frame, text="🎓 FHO Bot - Engenharia de Computação", 
                             font=('Arial', 16, 'bold'), bg='#1a1a1a', fg='#ecf0f1')
        title_label.pack(side=tk.LEFT, pady=10)
        
        # Botão de ajuda
        help_button = tk.Button(header_frame, text="❓", font=('Arial', 12), 
                              bg='#34495e', fg='white', bd=0, width=3,
                              command=self.show_help)
        help_button.pack(side=tk.RIGHT, pady=10, padx=(0, 5))
        
        # Separador
        separator = tk.Frame(self.root, height=2, bg='#34495e')
        separator.pack(fill='x', padx=10)
    
    def create_character_area(self):
        """Cria a área do personagem/avatar"""
        # Frame principal do personagem
        self.character_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.character_frame.pack(pady=15)
        
        # Avatar do bot (área circular com cor de estado)
        self.avatar_frame = tk.Frame(self.character_frame, bg=self.colors[BotState.IDLE], 
                                   width=650, height=650, relief='raised', bd=2)
        self.avatar_frame.pack_propagate(False)
        self.avatar_frame.pack()
        
        # Face do bot
        self.face_label = tk.Label(self.avatar_frame, text=self.faces[BotState.IDLE], 
                                 font=('Arial', 500), bg=self.colors[BotState.IDLE], fg='white')
        self.face_label.pack(expand=True)
        
        # Nome do bot
        self.bot_name_label = tk.Label(self.character_frame, text="FHO Bot", 
                                     font=('Arial', 14, 'bold'), bg='#1a1a1a', fg='#3498db')
        self.bot_name_label.pack(pady=(5, 0))
        
        # Estado atual em texto
        self.state_label = tk.Label(self.character_frame, text=self.state_descriptions[BotState.IDLE], 
                                  font=('Arial', 11), bg='#1a1a1a', fg='#bdc3c7')
        self.state_label.pack(pady=(2, 0))
    
    def create_controls(self):
        """Cria os controles da interface"""
        self.controls_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.controls_frame.pack(pady=10)
        
        # Botão de voz com estilo moderno
        self.voice_button = tk.Button(self.controls_frame, text="🎤 Falar (Ctrl+Enter)", 
                                    font=('Arial', 11, 'bold'), bg='#27ae60', fg='white',
                                    relief='flat', bd=0, padx=20, pady=8,
                                    command=self.on_voice_button_click)
        self.voice_button.pack(side=tk.LEFT, padx=5)
        
        # Botão de limpar conversa
        self.clear_button = tk.Button(self.controls_frame, text="🗑️ Limpar", 
                                    font=('Arial', 11), bg='#e74c3c', fg='white',
                                    relief='flat', bd=0, padx=15, pady=8,
                                    command=self.clear_conversation)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Botão de configurações
        self.settings_button = tk.Button(self.controls_frame, text="⚙️ Config", 
                                       font=('Arial', 11), bg='#95a5a6', fg='white',
                                       relief='flat', bd=0, padx=15, pady=8,
                                       command=self.show_settings)
        self.settings_button.pack(side=tk.LEFT, padx=5)
        
        # Botão de tela cheia
        self.fullscreen_button = tk.Button(self.controls_frame, text="⛶ Tela Cheia", 
                                         font=('Arial', 11), bg='#3498db', fg='white',
                                         relief='flat', bd=0, padx=15, pady=8,
                                         command=self.toggle_fullscreen)
        self.fullscreen_button.pack(side=tk.LEFT, padx=5)
        
        # Botão de tamanho do personagem
        self.character_size_button = tk.Button(self.controls_frame, text="📏 Tamanho Grande", 
                                             font=('Arial', 11), bg='#9b59b6', fg='white',
                                             relief='flat', bd=0, padx=15, pady=8,
                                             command=self.toggle_character_size)
        self.character_size_button.pack(side=tk.LEFT, padx=5)
    
    def create_text_input(self):
        """Cria a área de entrada de texto"""
        self.text_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.text_frame.pack(pady=10, padx=20, fill='x')
        
        # Label para o campo de entrada
        input_label = tk.Label(self.text_frame, text="Digite sua mensagem:", 
                             font=('Arial', 10), bg='#1a1a1a', fg='#bdc3c7')
        input_label.pack(anchor='w')
        
        # Frame para entrada e botão
        entry_frame = tk.Frame(self.text_frame, bg='#1a1a1a')
        entry_frame.pack(fill='x', pady=(5, 0))
        
        # Campo de entrada de texto
        self.text_entry = tk.Entry(entry_frame, font=('Arial', 12), bg='#34495e', fg='white',
                                 relief='flat', bd=5, insertbackground='white')
        self.text_entry.pack(side=tk.LEFT, fill='x', expand=True)
        self.text_entry.bind('<Return>', self.on_text_entry_return)
        
        # Botão enviar
        self.send_button = tk.Button(entry_frame, text="➤ Enviar", 
                                   font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                                   relief='flat', bd=0, padx=15,
                                   command=self.on_send_button_click)
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))
    
    def create_conversation_area(self):
        """Cria a área de conversação"""
        self.conversation_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.conversation_frame.pack(pady=(10, 0), padx=20, fill='both', expand=True)
        
        # Label para área de conversação
        conv_label = tk.Label(self.conversation_frame, text="Conversação:", 
                            font=('Arial', 10), bg='#1a1a1a', fg='#bdc3c7')
        conv_label.pack(anchor='w')
        
        # Área de texto scrollável para conversação
        self.conversation_text = scrolledtext.ScrolledText(
            self.conversation_frame, 
            font=('Consolas', 12),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white',
            wrap=tk.WORD,
            height=12,
            state=tk.DISABLED,
            relief='flat',
            bd=5
        )
        self.conversation_text.pack(fill='both', expand=True, pady=(5, 0))
        
        # Configurar tags para diferentes tipos de mensagem
        self.conversation_text.tag_configure("user", foreground="#3498db", font=('Consolas', 12, 'bold'))
        self.conversation_text.tag_configure("bot", foreground="#2ecc71", font=('Consolas', 12, 'bold'))
        self.conversation_text.tag_configure("system", foreground="#f39c12", font=('Consolas', 11, 'italic'))
        self.conversation_text.tag_configure("timestamp", foreground="#95a5a6", font=('Consolas', 9))
    
    def create_status_bar(self):
        """Cria a barra de status"""
        self.status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        self.status_frame.pack(fill='x', side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)
        
        # Status do TTS
        self.tts_status = tk.Label(self.status_frame, text="TTS: Carregando...", 
                                 font=('Arial', 9), bg='#34495e', fg='#bdc3c7')
        self.tts_status.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Contador de mensagens
        self.message_count = tk.Label(self.status_frame, text="Mensagens: 0", 
                                    font=('Arial', 9), bg='#34495e', fg='#bdc3c7')
        self.message_count.pack(side=tk.RIGHT, padx=10, pady=5)
        
        self.message_counter = 0
    
    def set_state(self, state: BotState):
        """
        Muda o estado visual do bot
        
        Args:
            state: Novo estado do bot
        """
        self.current_state = state
        
        # Atualizar cor de fundo do avatar
        color = self.colors[state]
        self.avatar_frame.configure(bg=color)
        self.face_label.configure(bg=color)
        
        # Atualizar emoji
        self.face_label.configure(text=self.faces[state])
        
        # Atualizar texto do estado
        self.state_label.configure(text=self.state_descriptions[state])
        
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
        
        # Efeito de pulso mudando o tamanho da fonte usando valores dinâmicos
        current_size = int(self.face_label.cget('font').split()[1])
        if current_size >= self.pulse_max:
            new_size = self.pulse_min
        else:
            new_size = self.pulse_max
            
        self.face_label.configure(font=('Arial', new_size))
        
        # Agendar próximo frame da animação
        self.root.after(600, self.pulse_animation)
    
    def add_message(self, sender: str, message: str):
        """
        Adiciona mensagem à área de conversação
        
        Args:
            sender: "user", "bot", ou "system"
            message: Texto da mensagem
        """
        self.conversation_text.configure(state=tk.NORMAL)
        
        # Adicionar timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Adicionar quebra de linha se não for a primeira mensagem
        if self.conversation_text.get(1.0, tk.END).strip():
            self.conversation_text.insert(tk.END, "\n")
        
        # Inserir timestamp
        self.conversation_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        if sender == "user":
            self.conversation_text.insert(tk.END, "Você: ", "user")
            self.message_counter += 1
        elif sender == "bot":
            self.conversation_text.insert(tk.END, "FHO Bot: ", "bot")
        else:
            self.conversation_text.insert(tk.END, "Sistema: ", "system")
        
        # Inserir mensagem
        self.conversation_text.insert(tk.END, f"{message}\n")
        
        # Scroll para o final
        self.conversation_text.see(tk.END)
        self.conversation_text.configure(state=tk.DISABLED)
        
        # Atualizar contador de mensagens
        self.message_count.configure(text=f"Mensagens: {self.message_counter}")
    
    def update_tts_status(self, status: str):
        """Atualiza o status do TTS na barra de status"""
        self.tts_status.configure(text=f"TTS: {status}")
    
    def clear_conversation(self):
        """Limpa a área de conversação"""
        if messagebox.askyesno("Limpar Conversação", "Deseja realmente limpar toda a conversação?"):
            self.conversation_text.configure(state=tk.NORMAL)
            self.conversation_text.delete(1.0, tk.END)
            self.conversation_text.configure(state=tk.DISABLED)
            self.message_counter = 0
            self.message_count.configure(text=f"Mensagens: {self.message_counter}")
    
    def show_settings(self):
        """Mostra janela de configurações"""
        messagebox.showinfo("Configurações", 
                           "Para alterar configurações, edite o arquivo config.yaml\n\n"
                           "Configurações disponíveis:\n"
                           "• Modelo LLM (deepseek, gemma3)\n"
                           "• Modo TTS (azure, sapi)\n"
                           "• Configurações de microfone\n"
                           "• Idioma e timeouts de voz")
    
    def show_help(self):
        """Mostra janela de ajuda"""
        help_text = """🤖 FHO Bot - Ajuda

COMO USAR:
• Digite mensagens no campo de texto e pressione Enter
• Clique em "🎤 Falar" ou pressione Ctrl+Enter para usar voz
• Use o botão "⛶ Tela Cheia" para alternar o modo de exibição
• O bot responde sobre Engenharia de Computação da FHO

ESTADOS VISUAIS:
😊 Azul: Aguardando (neutro)
👂 Verde: Escutando sua voz
🤔 Laranja: Processando resposta
😀 Azul claro: Falando resposta

BOTÕES:
• 🎤 Falar: Ativar microfone para entrada de voz
• 🗑️ Limpar: Limpar histórico de conversas
• ⚙️ Config: Abrir configurações
• ⛶ Tela Cheia: Alternar entre janela e tela cheia
• 📏 Tamanho: Alternar entre personagem grande (500) e médio (300)

ATALHOS:
• Enter: Enviar mensagem
• Ctrl+Enter: Ativar microfone
• F1: Esta ajuda
• Esc ou F11: Alternar tela cheia
• Ctrl+Q ou Alt+F4: Sair

DESENVOLVIDO PARA A FEIRA FHO 2024"""
        
        messagebox.showinfo("Ajuda - FHO Bot", help_text)
    
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
    
    def on_exit(self):
        """Callback para saída"""
        if messagebox.askyesno("Sair", "Deseja realmente sair do FHO Bot?"):
            self.close()
    
    def show_welcome_message(self):
        """Mostra mensagem de boas-vindas"""
        welcome = ("Olá! Eu sou seu assistente virtual da FHO. "
                  "Estou aqui para conversar com você sobre o curso de Engenharia de Computação!")
        self.add_message("bot", welcome)
        self.add_message("system", "💡 Dica: Digite sua pergunta ou use o botão 🎤 Falar para conversar por voz.")
    
    def run(self):
        """Inicia a interface visual"""
        self.show_welcome_message()
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.root.mainloop()
    
    def close(self):
        """Fecha a interface"""
        self.root.quit()
        self.root.destroy()

# Função de teste da interface aprimorada
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
        interface.add_message("user", "🎤 [Mensagem de voz capturada]")
        interface.set_state(BotState.THINKING)
        time.sleep(2)  # Simular processamento
        interface.set_state(BotState.SPEAKING)
        interface.add_message("bot", "Entendi sua mensagem de voz! Como posso ajudá-lo?")
        time.sleep(2)  # Simular fala
        interface.set_state(BotState.IDLE)
    
    # Criar e executar interface de teste aprimorada
    interface = EnhancedVisualInterface(on_text_input=test_text_input, on_voice_input=test_voice_input)
    interface.update_tts_status("Windows SAPI - Ativo")
    interface.run()
