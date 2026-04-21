from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
#from robot_tools import robot_tools

import yaml
from speech_to_text import SpeechToText
from text_to_speech import TTSManager
from rag_pipeline import get_context

# Carregar configurações
with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# Modelos disponíveis
MODELS = {
    "deepseek": "deepseek-r1:8b",
    "deepseek7b": "deepseek-r1:7b",
    "deepseek1.5b" : "deepseek-r1:1.5b",
    "gemma3": "gemma3:4b"
}

# Configurar modelo baseado no config
model_name = config['modelo']
if model_name not in MODELS:
    print(f"Erro: Modelo '{model_name}' não encontrado. Usando deepseek como padrão.")
    model_name = "deepseek"

model_llm = MODELS[model_name]

main_llm = ChatOllama(
    model=model_llm,
    temperature=config['llm']['temperatura'],
)

with open("prompts/main_prompt.yaml", "r", encoding="utf-8") as file:
    main_prompt = yaml.safe_load(file)['prompt']

main_prompt_template = PromptTemplate.from_template(main_prompt)

if __name__ == "__main__":
    # Inicializar STT e TTS Manager
    speech_to_text = SpeechToText()
    tts = TTSManager()
    
    # Mostrar informação simples do TTS
    print(tts.get_simple_info())
    print("FHO Bot: Olá! Eu sou seu assistente. Estou aqui para conversar com você sobre o curso de Engenharia de Computação da FHO!")
    print(speech_to_text.get_welcome_message())
    
    # Mensagem de boas-vindas também em voz
    welcome_message = "Olá! Eu sou seu assistente. Estou aqui para conversar com você sobre o curso de Engenharia de Computação da FHO!"
    tts.speak(welcome_message)
    
    while True:
        # Usar o stt para obter entrada do usuário
        user_input = speech_to_text.get_user_input()
        
        # Se retornou None, continua o loop (erro ou cancelamento)
        if user_input is None:
            continue
        
        if user_input.lower() == 'exit':
            farewell_message = "Adeus!"
            print(f"FHO Bot: {farewell_message}")
            tts.speak(farewell_message)
            break
        
        try:
            context = get_context(user_input) # Obter contexto relevante da RAG
            messages = [
                SystemMessage(content=f"{main_prompt}\n\nContexto:\n{context}"),
                HumanMessage(content=user_input)
            ]
            response = main_llm.invoke(messages)
            
            # Filtrar o <think> do DeepSeek-R1
            response_content = response.content
            if '<think>' in response_content and '</think>' in response_content:
                # Remove todo o bloco <think>...</think>
                import re
                response_content = re.sub(r'<think>.*?</think>', '', response_content, flags=re.DOTALL).strip()
            
            # Mostrar resposta no texto e falar
            print(f"FHO Bot: {response_content}")
            tts.speak(response_content)
            
        except Exception as e:
            error_message = f"Um erro ocorreu ao processar sua solicitação: {e}"
            print(f"FHO Bot: {error_message}")
            tts.speak("Desculpe, ocorreu um erro. Tente novamente.")
            print("Por favor, tente novamente ou reformule sua frase.")