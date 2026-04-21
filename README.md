# FHO Bot

Assistente virtual para apoio institucional e acadêmico do curso de Engenharia de Computação da FHO, com foco em atendimento na Feira de Profissões.

O projeto combina modelo local via Ollama, recuperação de contexto com RAG (ChromaDB) e interação multimodal (texto, fala e interface visual em Tkinter).

## Publicação em Repositório Público

Este repositório foi preparado para publicação pública. Conteúdo sensível foi removido e substituído por instruções de preenchimento.

Itens saneados:

- Chave real do Azure TTS removida de `config.yaml` e trocada por placeholder obrigatório.
- Artefatos locais gerados (`__pycache__/` e `chroma_db/`) removidos e ignorados via `.gitignore`.
- Arquivos privados de RAG (como PDFs internos) não são versionados; use a pasta `docs/rag_input/` localmente.

Antes de executar com Azure TTS, preencha a chave real da API no `config.yaml`.

## Objetivo do Projeto

O FHO Bot foi desenvolvido para:

- apresentar o curso de Engenharia de Computação da FHO de forma clara e acessível;
- responder dúvidas sobre grade curricular, informações gerais do curso e temas relacionados à área;
- manter um estilo didático, amigável e objetivo, adequado ao público da feira;
- operar com entrada e saída por voz, além de modo texto.

## Autoria

Projeto desenvolvido por: Victor Fiorio Casarin
e-mail: victor.fiorio.casarin@gmail.com
GitHub: https://github.com/VictorFiorioCasarin

## Principais Funcionalidades

- Respostas em português brasileiro com tom de professor acessível e comunicativo.
- Recuperação de contexto por RAG a partir dos arquivos em `docs/`.
- Suporte a diferentes modelos LLM locais no Ollama (DeepSeek e Gemma).
- Speech-to-Text com Google Speech Recognition e fallback offline (PocketSphinx).
- Text-to-Speech com dois provedores:
	- Windows SAPI (offline)
	- Azure Speech Services (neural, quando configurado)
- Duas formas de execução:
	- Modo texto (console)
	- Interface gráfica em Tkinter

## Arquitetura Resumida

Fluxo principal de resposta:

1. Usuário envia pergunta (texto ou voz).
2. O sistema busca contexto relevante na base vetorial (`rag_pipeline.py`).
3. O prompt principal é combinado com o contexto recuperado.
4. O LLM local no Ollama gera a resposta final.
5. A resposta é exibida em texto e, quando habilitado, convertida em áudio.

Componentes centrais:

- `main.py`: execução principal em modo texto.
- `Tkinter/main_enhanced.py`: execução com interface visual.
- `rag_pipeline.py`: carregamento documental, criação de chunks, embeddings e busca semântica.
- `speech_to_text.py`: captura e transcrição de voz.
- `text_to_speech/tts_manager.py`: seleção e gerenciamento do provedor TTS.
- `config.yaml`: configurações globais do projeto.
- `prompts/main_prompt.yaml`: regras de comportamento e estilo do assistente.

As regras de comportamento do assistente estão definidas em `prompts/main_prompt.yaml`.

## Requisitos

- Windows (projeto preparado com scripts `.bat`).
- Python 3.8 ou superior.
- Ollama instalado e em execução.
- Modelo de embeddings local disponível:
	- `nomic-embed-text`
- Pelo menos um modelo de resposta disponível no Ollama:
	- `deepseek-r1:8b` (padrão)
	- `deepseek-r1:7b`
	- `deepseek-r1:1.5b`
	- `gemma3:4b`

## Instalação

### Opção 1: scripts prontos (recomendado)

Na pasta `dependencias/`:

1. Execute `verificar-sistema.bat`.
2. Execute `instalar-dependencias.bat`.

### Opção 2: instalação manual

No diretório raiz do projeto:

```bash
python -m pip install --upgrade pip
python -m pip install -r dependencias/requirements.txt
```

Depois, baixe os modelos no Ollama:

```bash
ollama pull nomic-embed-text
ollama pull deepseek-r1:8b
```

## Execução

### Modo gráfico

Execute `fhobot.bat`.

Esse modo abre a interface em Tkinter, com interação por texto e voz.

### Modo texto

Execute `fhobot-text.bat`.

Esse modo roda no terminal e é útil para testes rápidos e depuração.

## Configuração

O arquivo `config.yaml` controla os principais parâmetros:

- `modelo`: modelo LLM usado pelo assistente.
- `llm.temperatura`: criatividade das respostas.
- `microfone`: modo de entrada de voz (`aberto`, `linha-de-comando`, `desligado` ou `desabilitado`).
- `tts.habilitado`: ativa ou desativa síntese de voz.
- `tts.modo`: seleciona `sapi` ou `azure`.
- `voz.*`: idioma e limites de captura de áudio.

### Configurando Azure TTS

Se desejar voz neural, configure em `config.yaml`:

```yaml
tts:
  modo: azure
  azure:
    api_key: "SUA_CHAVE_AQUI"
    regiao: "eastus2"
    voz: "pt-BR-FranciscaNeural"
```

Também é possível usar o guia interativo em `text_to_speech/azure_setup.py`.

Observação importante para repositório público:

- Não publique chaves reais no GitHub.
- Mantenha em `config.yaml` apenas placeholders, ou use um arquivo local não versionado, por exemplo `config.local.yaml`.

## Base de Conhecimento (RAG)

A recuperação de contexto utiliza os arquivos:

- `docs/sobre_o_curso.txt`
- `docs/informacoes_gerais_do_curso.txt`
- `docs/grade_curricular.json`

Para conteúdo privado de RAG (por exemplo, PDFs institucionais):

- Coloque os arquivos localmente em `docs/rag_input/`.
- Veja as instruções em `docs/rag_input/README.md`.
- Não publique esses arquivos em repositório público.

O pipeline cria embeddings, armazena dados em `chroma_db/` e aplica busca semântica para enriquecer as respostas.

## Comportamento Esperado do Assistente

As respostas devem seguir as diretrizes do prompt principal, incluindo:

- foco em Engenharia de Computação da FHO e contexto da Feira de Profissões;
- linguagem simples, didática e adequada ao público jovem;
- objetividade, concisão e uso de exemplos práticos quando pertinente;
- limitação de formato (respostas curtas, sem símbolos decorativos).

Se a pergunta estiver fora do escopo do projeto, o assistente deve informar a limitação e redirecionar para sua função principal.

## Estrutura do Projeto

```text
.
|-- main.py
|-- rag_pipeline.py
|-- speech_to_text.py
|-- robot_tools.py
|-- config.yaml
|-- .gitignore
|-- fhobot.bat
|-- fhobot-text.bat
|-- prompts/
|   `-- main_prompt.yaml
|-- docs/
|   |-- sobre_o_curso.txt
|   |-- informacoes_gerais_do_curso.txt
|   |-- grade_curricular.json
|   `-- rag_input/
|       `-- README.md
|-- text_to_speech/
|   |-- tts_manager.py
|   |-- windows_sapi_tts.py
|   |-- azure_tts.py
|   `-- azure_setup.py
|-- Tkinter/
|   |-- main_enhanced.py
|   `-- enhanced_visual.py
`-- dependencias/
    |-- requirements.txt
    |-- verificar-sistema.bat
    `-- instalar-dependencias.bat
```

## Solução de Problemas

- Erro de modelo no Ollama:
	- confirme se o modelo configurado em `config.yaml` foi baixado com `ollama pull`.
- Erro de dependências:
	- reinstale com `python -m pip install -r dependencias/requirements.txt`.
- Microfone não captura áudio:
	- revise `microfone` e `voz.*` em `config.yaml`.
- Sem áudio na resposta:
	- verifique `tts.habilitado` e `tts.modo`.
- Azure TTS indisponível:
	- valide chave, região e conectividade; o sistema pode cair para SAPI automaticamente.

## Segurança e Boas Práticas

- Não versione chaves de API reais em arquivos do repositório.
- Prefira variáveis de ambiente ou arquivos locais ignorados pelo Git para credenciais.
- Revise o prompt e a base de conhecimento antes de uso em evento para garantir consistência institucional.
- Mantenha arquivos privados de RAG fora do versionamento e carregue-os apenas em ambiente local.

