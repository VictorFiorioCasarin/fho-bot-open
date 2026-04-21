"""
Módulo TTS usando Windows SAPI (Speech API nativo)
Implementação mais confiável e sem dependências externas
"""

import subprocess
import yaml
import os
import tempfile


class WindowsSAPITTS:
    """Classe para Text-to-Speech usando Windows SAPI nativo"""
    
    def __init__(self, config_path="../config.yaml"):
        """
        Inicializa o TTS com Windows SAPI
        
        Args:
            config_path (str): Caminho para o arquivo de configuração
        """
        # Resolve the config path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_full_path = os.path.join(current_dir, config_path)
        
        with open(config_full_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)
    
    def get_tts_config(self):
        """Retorna se o TTS está habilitado"""
        return self.config.get('tts', {}).get('habilitado', True)
    
    def list_available_voices(self):
        """
        Lista todas as vozes disponíveis no sistema
        
        Returns:
            list: Lista de vozes instaladas
        """
        try:
            ps_command = '''
            Add-Type -AssemblyName System.Speech;
            $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
            $synth.GetInstalledVoices() | ForEach-Object { 
                $_.VoiceInfo.Name + " | " + $_.VoiceInfo.Culture + " | " + $_.VoiceInfo.Gender 
            }
            '''
            
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                voices = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split(' | ')
                        if len(parts) >= 3:
                            voices.append({
                                'name': parts[0],
                                'culture': parts[1],
                                'gender': parts[2]
                            })
                return voices
            else:
                print(f"TTS: Erro ao listar vozes: {result.stderr}")
                return []
                
        except Exception as e:
            print(f"TTS: Erro ao listar vozes: {e}")
            return []
    
    def get_best_portuguese_voice(self, voice_preference=None):
        """
        Encontra a melhor voz em português baseada na configuração
        
        Args:
            voice_preference: Nome específico da voz, 'feminina', 'masculina' ou None (usar config)
        
        Returns:
            str: Nome da melhor voz PT-BR ou None
        """
        voices = self.list_available_voices()
        
        # Use o parâmetro se fornecido, senão use a configuração
        if voice_preference is None:
            voice_preference = self.config.get('tts', {}).get('tipo_voz', 'feminina')
        
        # Filtrar vozes portuguesas
        pt_voices = []
        for voice in voices:
            culture = voice['culture'].lower()
            if 'pt-br' in culture or ('portuguese' in culture and 'brazil' in culture):
                pt_voices.append(voice)
        
        if not pt_voices:
            return None
        
        # Se foi especificado um nome de voz específico
        if voice_preference not in ['feminina', 'masculina', 'auto']:
            for voice in pt_voices:
                if voice_preference.lower() in voice['name'].lower():
                    return voice['name']
            
            # Se não encontrou, tentar inferir por gênero baseado no nome
            if voice_preference.lower() in ['daniel', 'ricardo', 'carlos', 'rafael']:
                voice_preference = 'masculina'
            elif voice_preference.lower() in ['maria', 'heloisa', 'helena', 'ana', 'lucia']:
                voice_preference = 'feminina'
            else:
                voice_preference = 'auto'
        
        # Aplicar preferência de gênero
        if voice_preference == 'feminina':
            # Procurar vozes femininas primeiro
            for voice in pt_voices:
                name = voice['name'].lower()
                gender = voice['gender'].lower()
                if ('female' in gender or 'maria' in name or 'helena' in name or 
                    'heloisa' in name or 'ana' in name):
                    return voice['name']
        
        elif voice_preference == 'masculina':
            # Procurar vozes masculinas primeiro
            for voice in pt_voices:
                name = voice['name'].lower()
                gender = voice['gender'].lower()
                if ('male' in gender or 'daniel' in name or 'rafael' in name or 
                    'ricardo' in name or 'carlos' in name):
                    return voice['name']
        
        # Fallback: primeira voz portuguesa disponível
        selected_voice = pt_voices[0]['name']
        return selected_voice
    
    def speak(self, text):
        """
        Converte texto em fala usando Windows SAPI (método otimizado para textos longos)
        
        Args:
            text (str): Texto para ser falado
        """
        if not self.get_tts_config():
            return False
        
        if not text or not text.strip():
            return False
        
        try:
            # Limpar texto
            clean_text = self._clean_text(text)
            
            # Usar sempre o método de divisão em sentenças (mais confiável)
            self._speak_long_text(clean_text)
            return True
                
        except Exception as e:
            return False
    
    def _speak_long_text(self, text):
        """
        Fala textos dividindo em sentenças (método principal)
        
        Args:
            text (str): Texto para ser falado
        """
        try:
            # Obter configurações
            rate = self.config.get('tts', {}).get('sapi', {}).get('velocidade', 0)
            volume = int(self.config.get('tts', {}).get('sapi', {}).get('volume', 0.8) * 100)
            
            # Certificar que rate é um integer válido (-10 a +10)
            if isinstance(rate, str):
                # Se for string, tentar extrair número
                rate = int(''.join(filter(lambda x: x.isdigit() or x == '-', str(rate))) or 0)
            rate = max(-10, min(10, int(rate)))  # Limitar entre -10 e +10
            
            # Encontrar melhor voz
            voice_name = self.get_best_portuguese_voice()
            voice_select = f"$synth.SelectVoice('{voice_name}');" if voice_name else ""
            
            # Dividir texto em sentenças
            sentences = text.replace('.', '.|').replace('!', '!|').replace('?', '?|').split('|')
            
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence and len(sentence) > 3:
                    # Comando completo para cada sentença
                    command = f'''
                    Add-Type -AssemblyName System.Speech;
                    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
                    {voice_select}
                    $synth.Rate = {rate};
                    $synth.Volume = {volume};
                    $synth.Speak("{self._escape_for_powershell(sentence)}");
                    '''
                    
                    subprocess.run(
                        ["powershell", "-Command", command],
                        capture_output=True,
                        text=True,
                        timeout=15
                    )
            
        except Exception as e:
            pass
    
    def _clean_text(self, text):
        """
        Limpa texto para melhor pronunciação
        
        Args:
            text (str): Texto original
            
        Returns:
            str: Texto limpo
        """
        # Remover prefixos
        clean_text = text.replace("FHO Bot:", "").strip()
        
        # Substituições para melhor pronunciação
        replacements = {
            "FHO": "F H Ó",
            "TI": "T I",
            "AI": "A I",
            "IA": "Í A",
            "API": "A P I",
            "3D": "três D",
            "2D": "dois D",
            "&": " e ",
            "@": " arroba ",
            "%": " por cento ",
            "vs": " versus ",
            "etc": " etcétera ",
            "python": "paiton",
            "Python": "Paiton",
            "C#": "C charpi",
            "C++": "C mais mais",
            "JavaScript": "Java script"
        }
        
        for old, new in replacements.items():
            clean_text = clean_text.replace(old, new)
        
        return clean_text.strip()
    
    def _escape_for_powershell(self, text):
        """
        Escapa texto para uso seguro no PowerShell
        
        Args:
            text (str): Texto original
            
        Returns:
            str: Texto escapado
        """
        # Escapar caracteres especiais do PowerShell
        escaped = text.replace('"', '""')  # Aspas duplas
        escaped = escaped.replace('`', '``')  # Backticks
        escaped = escaped.replace('$', '`$')  # Cifrão
        
        return escaped
    
    def test_voice(self):
        """Testa a configuração de voz atual"""
        print("=== Teste Windows SAPI TTS ===")
        
        # Listar vozes
        print("\nVozes disponíveis:")
        voices = self.list_available_voices()
        for voice in voices:
            print(f"  - {voice['name']} ({voice['culture']}) - {voice['gender']}")
        
        # Mostrar voz selecionada
        best_voice = self.get_best_portuguese_voice()
        print(f"\nVoz selecionada: {best_voice}")
        
        # Teste de fala
        test_text = "Olá! Este é um teste do sistema de voz do Windows SAPI. Posso falar sobre Engenharia de Computação!"
        print(f"\nTestando: '{test_text}'")
        self.speak(test_text)
        
        print("\n✅ Teste concluído!")
