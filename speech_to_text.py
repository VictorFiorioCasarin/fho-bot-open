"""
Módulo responsável por toda a funcionalidade de Speech-to-Text do FHO Bot.
Gerencia entrada de voz, configurações de microfone e processamento de áudio.
"""

import speech_recognition as sr
import yaml


class SpeechToText:
    
    def __init__(self, config_path="config.yaml"):
        """
        Inicializa o handler de voz com as configurações do arquivo YAML
        """
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def get_microphone_config(self):
        """Retorna a configuração atual do microfone"""
        return self.config.get('microfone', 'linha-de-comando')
    
    def speech_to_text(self, open_mode=False):
        """
        Captura áudio do microfone e converte para texto
        
        Args:
            open_mode (bool): Se True, não usa timeout (para modo aberto)
        
        Returns:
            str or None: Texto reconhecido ou None se falhou
        """
        print("FHO Bot: Ajustando microfone... aguarde.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        if open_mode:
            print("FHO Bot: Escutando... (fale quando quiser)")
        else:
            print("FHO Bot: Pode falar agora! (Pressione Ctrl+C para cancelar)")
        
        try:
            with self.microphone as source:
                if open_mode:
                    # Modo aberto: sem timeout para começar, apenas limite de frase
                    tempo_max = self.config['voz']['tempo_maximo']
                    audio = self.recognizer.listen(source, phrase_time_limit=tempo_max)
                else:
                    # Modo normal: com timeout
                    timeout = self.config['voz']['timeout_inicio']
                    tempo_max = self.config['voz']['tempo_maximo']
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=tempo_max)
            
            print("FHO Bot: Processando sua fala...")
            
            # Tenta reconhecer usando o Google Speech Recognition (funciona offline com PocketSphinx como fallback)
            try:
                idioma = self.config['voz']['idioma']
                text = self.recognizer.recognize_google(audio, language=idioma)
                return text
            except sr.RequestError:
                # Se não conseguir usar Google, usa PocketSphinx offline
                print("FHO Bot: Usando reconhecimento offline...")
                text = self.recognizer.recognize_sphinx(audio, language=idioma)
                return text
                
        except sr.WaitTimeoutError:
            print("FHO Bot: Tempo esgotado. Nenhuma fala detectada.")
            return None
        except sr.UnknownValueError:
            print("FHO Bot: Não consegui entender o que você disse. Tente novamente.")
            return None
        except KeyboardInterrupt:
            print("\nFHO Bot: Captura de voz cancelada.")
            return None
        except Exception as e:
            print(f"FHO Bot: Erro ao capturar áudio: {e}")
            return None
    
    def get_user_input(self):
        """
        Gerencia entrada do usuário baseada na configuração do microfone
        
        Returns:
            str or None: Input do usuário ou None se deve continuar loop
        """
        microfone_config = self.get_microphone_config()
        
        if microfone_config == 'aberto':
            # Modo aberto: sempre tenta capturar voz primeiro (sem timeout)
            print("\nFHO Bot: Escutando... (ou pressione Ctrl+C e digite sua mensagem)")
            user_input = self.speech_to_text(open_mode=True)
            if user_input is None:
                # Se não capturou áudio, permite entrada de texto
                user_input = input("Você (texto): ")
            else:
                print(f"Você disse: {user_input}")
            return user_input
            
        else:
            # Outros modos: entrada de texto primeiro
            user_input = input("\nVocê: ")
            
            if user_input.lower() == 'falar' and microfone_config == 'linha-de-comando':
                # Aguardar e capturar entrada de voz
                user_input = self.speech_to_text()
                if user_input is None:
                    return None  # Indica para continuar o loop
                print(f"Você disse: {user_input}")
                return user_input
                
            elif user_input.lower() == 'falar' and microfone_config == 'desligado':
                print("FHO Bot: Microfone está desabilitado nas configurações. Edite config.yaml para ativar.")
                return None  # Indica para continuar o loop
                
            return user_input
    
    def get_welcome_message(self):
        """
        Retorna a mensagem de boas-vindas baseada na configuração do microfone
        """
        microfone_config = self.get_microphone_config()
        
        if microfone_config == 'aberto':
            return "Microfone sempre ativo - fale diretamente (sem limite de tempo) ou pressione Ctrl+C e digite. (Digite 'exit' para sair)"
        elif microfone_config == 'linha-de-comando':
            return "Digite sua mensagem ou 'falar' para usar voz. (Digite 'exit' para sair)"
        elif microfone_config == 'desligado':
            return "Digite sua mensagem. (Digite 'exit' para sair)"
        else:
            return "Digite sua mensagem ou 'falar' para voz. (Digite 'exit' para sair)"
    
    def get_stt_info(self):
        """
        Retorna informações sobre o serviço STT disponível
        
        Returns:
            str: Descrição do serviço STT (Google online ou PocketSphinx offline)
        """
        try:
            # Tenta fazer um teste rápido para ver se Google está disponível
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return f"Google Speech Recognition - {self.get_microphone_config()}"
        except:
            # Se não conseguir conectar, assume offline
            return f"PocketSphinx (offline) - {self.get_microphone_config()}"
    
    def get_voice_input(self):
        """
        Método específico para captura de voz (usado pela interface visual)
        
        Returns:
            str or None: Texto reconhecido ou None se falhou
        """
        return self.speech_to_text(open_mode=False)
