import requests
from langchain.tools import tool
import json
import yaml

# Importando o parser JSON que o LangChain usa internamente para ser mais robusto
from langchain.output_parsers import json as json_parser_lc # Importa o módulo json do langchain.output_parsers

# Carregar o prompt do classificador a partir do arquivo YAML
with open('Prompts/tools_prompt.yaml', 'r') as file:
    tools_prompt = yaml.safe_load(file)['prompt']

@tool
def test_tool(sentence: str) -> str:
    """
    Ferramente utilizada para testes que retorna se o uso da ferramente foi um sucesso.
    """
    return f"Teste de ferramenta bem-sucedido com a frase: {sentence}"

robot_tools = [test_tool]