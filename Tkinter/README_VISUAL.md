# 🤖 FHO Bot - Interface Visual

## 📋 Visão Geral

O FHO Bot agora possui uma interface visual moderna e interativa desenvolvida com Tkinter, oferecendo uma experiência visual rica com estados animados e feedback em tempo real.

## 🎨 Funcionalidades Visuais

### Estados Visuais do Bot
- **😊 NEUTRO (Azul)**: Bot aguardando interação
- **👂 ESCUTANDO (Verde)**: Capturando entrada de voz (STT)
- **🤔 PENSANDO (Laranja)**: Processando com IA (LLM)
- **😀 FALANDO (Azul Claro)**: Reproduzindo resposta (TTS)

### Animações
- **Pulso**: Avatar do bot pulsa durante estados ativos
- **Cores Dinâmicas**: Fundo muda conforme o estado
- **Transições Suaves**: Mudanças visuais fluidas

### Interface Moderna
- **Avatar Circular**: Personagem visual com emoji expressivo
- **Área de Conversação**: Chat scrollável com timestamps
- **Controles Intuitivos**: Botões para voz, texto e configurações
- **Barra de Status**: Informações sobre TTS e contadores
- **Atalhos de Teclado**: Navegação rápida

## 📁 Estrutura de Arquivos

```
fho-bot/
├── Tkinter/                 # Interface visual organizada
│   ├── visual_interface.py      # Interface visual básica
│   ├── enhanced_visual.py       # Interface visual aprimorada
│   ├── main_visual.py          # Bot com interface básica
│   ├── main_enhanced.py        # Bot com interface aprimorada
│   ├── demo_visual.py          # Demonstração das funcionalidades
│   └── test_interface.py       # Teste básico da interface
├── text_to_speech/         # Módulo TTS organizado
│   ├── tts_manager.py
│   ├── azure_tts.py
│   ├── windows_sapi_tts.py
│   └── ...
├── main.py                 # Bot original (console)
├── speech_to_text.py       # Módulo STT
├── rag_pipeline.py         # Pipeline RAG
└── config.yaml             # Configurações
```

## 🚀 Como Executar

### 1. Versão Básica
```bash
cd Tkinter
python main_visual.py
```

### 2. Versão Aprimorada (Recomendada)
```bash
cd Tkinter
python main_enhanced.py
```

### 3. Demonstração Visual
```bash
cd Tkinter
python demo_visual.py
```

### 4. Teste da Interface
```bash
cd Tkinter
python test_interface.py
```
```bash
python main_enhanced.py
```

### 3. Demonstração Visual
```bash
python demo_visual.py
```

### 4. Teste de Interface (Standalone)
```bash
python enhanced_visual.py
```

## ⚙️ Configuração

As configurações visuais são automáticas, mas você pode ajustar:

- **config.yaml**: Configurações de TTS, STT e modelo LLM
- **Cores**: Modificar no código (`enhanced_visual.py`)
- **Animações**: Ajustar velocidade e estilo

## 🎯 Funcionalidades da Interface

### Entrada de Dados
- **Texto**: Digite e pressione Enter
- **Voz**: Clique no botão 🎤 ou Ctrl+Enter
- **Comandos**: 'exit', 'sair', 'tchau' para finalizar

### Atalhos de Teclado
- **Enter**: Enviar mensagem de texto
- **Ctrl+Enter**: Ativar captura de voz
- **F1**: Mostrar ajuda
- **Esc**: Sair da aplicação

### Controles da Interface
- **🎤 Falar**: Capturar entrada de voz
- **🗑️ Limpar**: Limpar histórico de conversação
- **⚙️ Config**: Informações sobre configuração
- **❓ Ajuda**: Guia de uso

## 📊 Status e Feedback

### Indicadores Visuais
- **Avatar**: Muda cor e expressão conforme estado
- **Texto de Status**: Descrição textual do estado atual
- **Contador de Mensagens**: Número de interações
- **Status do TTS**: Método TTS ativo (Azure/SAPI)

### Área de Conversação
- **Timestamps**: Horário de cada mensagem
- **Cores Diferenciadas**: 
  - Azul: Mensagens do usuário
  - Verde: Respostas do bot
  - Laranja: Mensagens do sistema
- **Scroll Automático**: Sempre mostra última mensagem

## 🔧 Tecnologias Utilizadas

### Interface
- **Tkinter**: Framework GUI nativo do Python
- **Threading**: Processamento assíncrono para UI responsiva
- **Enum**: Gerenciamento de estados

### Integração
- **LangChain + Ollama**: Processamento de IA
- **Speech Recognition**: Captura de voz
- **Azure TTS / Windows SAPI**: Síntese de voz
- **YAML**: Configurações

## 📱 Design Responsivo

- **Janela Centralizada**: Posicionamento automático
- **Cores Escuras**: Interface moderna e confortável
- **Fontes Legíveis**: Tamanhos adequados para apresentação
- **Layout Fixo**: Otimizado para demonstrações

## 🎪 Para Apresentações

### Modo Demonstração
```bash
python demo_visual.py
```

- Sequência automática de perguntas
- Simulação completa de todos os estados
- Respostas pré-definidas sobre Engenharia de Computação
- Ideal para feiras e apresentações

### Dicas para Apresentação
1. **Execute `main_enhanced.py`** para versão completa
2. **Use o modo voz** para impressionar audiência
3. **Mostre os estados visuais** explicando cada cor
4. **Demonstre diferentes tipos de perguntas**
5. **Destaque a integração com IA**

## ⚠️ Requisitos

### Software
- Python 3.8+
- Tkinter (incluso no Python)
- Dependências do FHO Bot (LangChain, Ollama, etc.)

### Hardware
- Microfone (para entrada de voz)
- Alto-falantes ou fones (para TTS)
- Tela com resolução mínima 800x600

## 🐛 Solução de Problemas

### Interface não abre
- Verificar se Tkinter está instalado
- Executar: `python -m tkinter`

### Erro de importação
- Verificar se todos os módulos estão no diretório
- Executar do diretório correto do projeto

### TTS não funciona
- Verificar configurações em `config.yaml`
- Testar: `python -c "from text_to_speech.tts_manager import TTSManager; TTSManager().speak('teste')"`

### Microfone não detecta
- Verificar permissões do microfone
- Testar configuração em `config.yaml`

## 🎉 Conclusão

A interface visual do FHO Bot oferece uma experiência moderna e profissional, perfeita para demonstrações em feiras educacionais. Com estados visuais claros, animações suaves e feedback em tempo real, o bot proporciona uma interação natural e envolvente com os visitantes.

---

**Desenvolvido para a Feira FHO 2024**  
*Demonstrando o futuro da educação em Engenharia de Computação*
