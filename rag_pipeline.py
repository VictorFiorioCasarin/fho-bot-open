from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import json

# Nota para uso em repositório público:
# PDFs e outros documentos privados para RAG devem ficar em docs/rag_input/ (não versionado).
# Este pipeline padrão usa apenas os arquivos públicos versionados em docs/.

# 1. Carregar conteúdo do arquivo sobre o curso
# 1.1 Arquivo sobre_o_curso.txt
file_loader = TextLoader("docs/sobre_o_curso.txt", encoding="utf-8")
file_docs = file_loader.load()

# Adicionar metadados aos documentos do arquivo texto
for doc in file_docs:
    doc.metadata.update({
        "source": "sobre_o_curso.txt",
        "tipo": "informacoes_curso"
    })

# 1.2 Arquivo informacoes_gerais_do_curso.txt
info_loader = TextLoader("docs/informacoes_gerais_do_curso.txt", encoding="utf-8")
info_docs = info_loader.load()

for doc in info_docs:
    doc.metadata.update({
        "source": "informacoes_gerais_do_curso.txt",
        "tipo": "informacoes_curso"
    })

# 2. Carregar arquivo json e processar adequadamente
with open("docs/grade_curricular.json", "r", encoding="utf-8") as f:
    grade_data = json.load(f)

# 3. Criar documentos estruturados para cada período
grade_docs = []
for periodo_info in grade_data["Periodos"]:
    periodo_num = periodo_info["Periodo"]
    
    # Criar documento formatado para melhor busca
    content = f"Período {periodo_num}:\n\n"
    
    materias_list = []
    for materia in periodo_info["Materias"]:
        materias_list.append(f"- {materia['Nome']} ({materia['Codigo']}) - {materia['Carga_Horaria']}h")
    
    content += "\n".join(materias_list)
    
    # Adicionar versões alternativas para melhor busca
    content += f"\n\nEste é o {periodo_num}° período da grade curricular do curso de Engenharia da Computação."
    
    # Mapear números para palavras
    numeros_por_extenso = {
        1: "primeiro", 2: "segundo", 3: "terceiro", 4: "quarto", 5: "quinto",
        6: "sexto", 7: "sétimo", 8: "oitavo", 9: "nono", 10: "décimo",
        11: "décimo primeiro", 12: "décimo segundo"
    }
    
    if periodo_num in numeros_por_extenso:
        content += f"\nMatérias do {numeros_por_extenso[periodo_num]} período:"
        content += f"\nDisciplinas do {numeros_por_extenso[periodo_num]} semestre:"
        content += f"\n{numeros_por_extenso[periodo_num].capitalize()} período: {len(materias_list)} matérias"
    
    # Criar documento do LangChain
    from langchain.schema import Document
    doc = Document(
        page_content=content,
        metadata={
            "source": "grade_curricular.json",
            "periodo": periodo_num,
            "tipo": "grade_curricular"
        }
    )
    grade_docs.append(doc)

# 4. Juntar documentos
all_docs = grade_docs + file_docs + info_docs

# 5. Dividir em chunks (com configurações otimizadas)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,  # Aumentar para manter períodos completos
    chunk_overlap=100,  # Reduzir overlap
    separators=["\n\n", "\n", ".", "!", "?", ";", ":", " ", ""]
)
chunks = splitter.split_documents(all_docs)

# 6. Gerar embeddings e armazenar no ChromaDB
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

# 7. Função para normalizar consultas e melhorar busca (melhorada)
def normalize_query(query):
    """
    Normaliza a consulta do usuário para melhorar a busca vetorial
    Retorna múltiplas versões da consulta para busca abrangente
    """
    query_lower = query.lower()
    
    # Mapeamento de períodos por extenso para números
    period_mapping = {
        'primeiro período': ['primeiro período', 'período 1', 'periodo 1', '1° período', '1º período'],
        'segundo período': ['segundo período', 'período 2', 'periodo 2', '2° período', '2º período'],
        'terceiro período': ['terceiro período', 'período 3', 'periodo 3', '3° período', '3º período'],
        'quarto período': ['quarto período', 'período 4', 'periodo 4', '4° período', '4º período'],
        'quinto período': ['quinto período', 'período 5', 'periodo 5', '5° período', '5º período'],
        'sexto período': ['sexto período', 'período 6', 'periodo 6', '6° período', '6º período'],
        'sétimo período': ['sétimo período', 'período 7', 'periodo 7', '7° período', '7º período'],
        'oitavo período': ['oitavo período', 'período 8', 'periodo 8', '8° período', '8º período'],
        'nono período': ['nono período', 'período 9', 'periodo 9', '9° período', '9º período'],
        'décimo período': ['décimo período', 'período 10', 'periodo 10', '10° período', '10º período'],
        'décimo primeiro': ['décimo primeiro período', 'período 11', 'periodo 11', '11° período', '11º período'],
        'décimo segundo': ['décimo segundo período', 'período 12', 'periodo 12', '12° período', '12º período'],
    }
    
    # Verificar se a consulta menciona um período específico (por extenso)
    for periodo_extenso, variacoes in period_mapping.items():
        if any(termo in query_lower for termo in [periodo_extenso, periodo_extenso.replace('período', 'periodo')]):
            return variacoes
    
    # Verificar se a consulta menciona um período específico (direto por número)
    import re
    periodo_numero_pattern = r'periodo\s*(\d+)|período\s*(\d+)|(\d+)\s*periodo|(\d+)\s*período'
    match = re.search(periodo_numero_pattern, query_lower)
    
    if match:
        # Extrair o número do período
        numero = match.group(1) or match.group(2) or match.group(3) or match.group(4)
        if numero and 1 <= int(numero) <= 12:
            # Retornar variações para o período específico
            numeros_por_extenso = {
                '1': 'primeiro', '2': 'segundo', '3': 'terceiro', '4': 'quarto', '5': 'quinto',
                '6': 'sexto', '7': 'sétimo', '8': 'oitavo', '9': 'nono', '10': 'décimo',
                '11': 'décimo primeiro', '12': 'décimo segundo'
            }
            extenso = numeros_por_extenso.get(numero, '')
            return [
                f'{extenso} período',
                f'período {numero}',
                f'periodo {numero}',
                f'{numero}° período',
                f'{numero}º período'
            ]
    
    # Se não encontrou período específico, normalizar termos gerais
    normalizations = {
        'matérias': 'materias',
        'disciplinas': 'materias', 
        'cadeiras': 'materias',
        'disciplina': 'materia',
        'semestre': 'periodo',
        'semestres': 'periodos',
    }
    
    for term, replacement in normalizations.items():
        query_lower = query_lower.replace(term, replacement)
    
    return [query_lower]

# 8. Função para buscar contexto relevante (completamente reformulada)
def get_context(query):
    """
    Busca contexto relevante usando múltiplas estratégias
    """
    # Obter variações da consulta normalizada
    query_variations = normalize_query(query)
    
    # Combinar todos os resultados únicos
    all_results = []
    seen_content = set()
    
    # Fazer busca com cada variação da consulta
    for variation in query_variations:
        results = vectorstore.similarity_search(variation, k=3)
        for doc in results:
            if doc.page_content not in seen_content:
                all_results.append(doc)
                seen_content.add(doc.page_content)
    
    # Se não encontrou resultados com variações, tentar busca original
    if not all_results:
        results = vectorstore.similarity_search(query, k=4)
        all_results = results
    
    # Priorizar documentos da grade curricular se a consulta for sobre períodos/matérias
    # OU documentos de informações do curso para consultas gerais sobre o curso
    if any(termo in query.lower() for termo in ['período', 'periodo', 'matéria', 'materias', 'disciplina', 'disciplinas']):
        grade_results = []
        info_curso_results = []
        other_results = []
        
        for doc in all_results:
            doc_tipo = doc.metadata.get('tipo', '')
            if 'grade_curricular' in doc_tipo:
                grade_results.append(doc)
            elif 'informacoes_curso' in doc_tipo:
                info_curso_results.append(doc)
            else:
                other_results.append(doc)
        
        # NOVA LÓGICA: Se query menciona período específico, priorizar esse período
        import re
        # Detectar se query menciona período específico
        periodo_mencionado = None
        
        # Por extenso
        periodos_extenso = {
            'primeiro': 1, 'segundo': 2, 'terceiro': 3, 'quarto': 4, 'quinto': 5,
            'sexto': 6, 'sétimo': 7, 'oitavo': 8, 'nono': 9, 'décimo': 10
        }
        for extenso, numero in periodos_extenso.items():
            if extenso in query.lower():
                periodo_mencionado = numero
                break
        
        # Por número direto
        if not periodo_mencionado:
            match = re.search(r'periodo\s*(\d+)|período\s*(\d+)|(\d+)\s*periodo|(\d+)\s*período', query.lower())
            if match:
                numero_str = match.group(1) or match.group(2) or match.group(3) or match.group(4)
                if numero_str and 1 <= int(numero_str) <= 12:
                    periodo_mencionado = int(numero_str)
        
        # Se detectou período específico, priorizar documentos desse período
        if periodo_mencionado:
            periodo_especifico = []
            outros_periodos = []
            
            for doc in grade_results:
                if doc.metadata.get('periodo') == periodo_mencionado:
                    periodo_especifico.append(doc)
                else:
                    outros_periodos.append(doc)
            
            # Priorizar: período específico -> outros períodos -> info curso -> outros
            all_results = periodo_especifico + outros_periodos + info_curso_results + other_results
        else:
            # Sem período específico, priorizar grade curricular
            all_results = grade_results + info_curso_results + other_results
    
    # Para consultas sobre informações gerais do curso (coordenador, mensalidade, etc.)
    elif any(termo in query.lower() for termo in ['coordenador', 'professor', 'mensalidade', 'bolsa', 'duração', 'carga horária', 'sobre o curso', 'objetivo']):
        info_curso_results = []
        grade_results = []
        other_results = []
        
        for doc in all_results:
            doc_tipo = doc.metadata.get('tipo', '')
            if 'informacoes_curso' in doc_tipo:
                info_curso_results.append(doc)
            elif 'grade_curricular' in doc_tipo:
                grade_results.append(doc)
            else:
                other_results.append(doc)
        
        # Priorizar: informações do curso -> grade curricular -> outros
        all_results = info_curso_results + grade_results + other_results
    
    # Limitar a 4 resultados mais relevantes
    final_results = all_results[:4]
    
    return "\n\n".join([doc.page_content for doc in final_results])

# 9. Função para debug - verificar se período está no banco
def debug_period_search(period_number):
    """
    Função de debug para verificar se um período específico está no banco
    """
    searches = [
        f"período {period_number}",
        f"periodo {period_number}",
        f"Período {period_number}",
    ]
    
    print(f"Debug: Procurando período {period_number}")
    for search in searches:
        results = vectorstore.similarity_search(search, k=2)
        print(f"  Busca '{search}': {len(results)} resultados")
        for i, doc in enumerate(results):
            preview = doc.page_content[:100].replace('\n', ' ')
            print(f"    {i+1}: {preview}...")

if __name__ == "__main__":
    # Teste rápido do sistema
    print("Sistema RAG atualizado carregado com sucesso!")
    print("\nTestando busca por períodos:")
    
    test_queries = [
        "Quais as matérias do segundo período?",
        "Quais as materias do terceiro periodo?",
        "primeiro período",
        "materias periodo 4"
    ]
    
    for query in test_queries:
        print(f"\nConsulta: {query}")
        context = get_context(query)
        print(f"Contexto (primeiros 200 chars): {context[:200]}...")