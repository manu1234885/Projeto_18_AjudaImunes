
# Ajuda Imunes AI Coder - Assistente de Programação Python

# Importa as bibliotecas necessárias
import streamlit as st
from groq import Groq


# Configura a página do Streamlit
st.set_page_config(
    page_title="Ajuda Imunes AI Coder",
    page_icon="💁‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Define as instruções do assistente de IA
CUSTOM_PROMPT = """
Você é o "Ajuda Imunes AI Coder", um assistente de IA
especialista em programação, com foco principal em Python.

Sua missão é ajudar desenvolvedores iniciantes com dúvidas
de programação de forma clara, precisa e útil.

REGRAS DE OPERAÇÃO:

1. FOCO EM PROGRAMAÇÃO:
Responda apenas a perguntas relacionadas à programação,
algoritmos, estruturas de dados, bibliotecas e frameworks.
Se a pergunta for sobre outro assunto, explique educadamente
que seu foco é auxiliar com programação.

2. ESTRUTURA DA RESPOSTA:
- Explicação clara do conceito.
- Exemplo de código Python comentado.
- Explicação de cada parte do código.
- Seção "📚 Documentação de Referência" com links oficiais
  relevantes para Python ou para a biblioteca utilizada.

3. CLAREZA E PRECISÃO:
Use linguagem simples e didática, evitando termos técnicos
desnecessários. Garanta que os exemplos estejam corretos.
"""


# Cria a barra lateral
with st.sidebar:
    st.title("💁‍♀️ Ajuda todas as minorias ")

    st.markdown(
        "Um assistente de IA focado em programação Python "
        "para ajudar iniciantes."
    )

    # Campo para inserir a chave da API
    groq_api_key = st.text_input(
        "Insira sua API Key Groq",
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )

    st.markdown("---")

    st.markdown(
        "Desenvolvido para auxiliar em suas dúvidas de "
        "programação em Python. A IA pode cometer erros; "
        "sempre confira a documentação."
    )

    st.markdown("---")

    st.markdown(
        "Conheça os cursos, formações e programas de "
        "pós-graduação da DSA."
    )


# Título e descrição do aplicativo
st.title("Ajuda Imunes AI Coder")

st.subheader("Assistente Pessoal de Programação Python 🐍")

st.caption(
    "Faça sua pergunta sobre Python e receba códigos, "
    "explicações e referências."
)


# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []


# Exibe as mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Inicializa o cliente da Groq
client = None

if groq_api_key:
    try:
        client = Groq(api_key=groq_api_key)

    except Exception as e:
        st.sidebar.error(
            f"Erro ao inicializar o cliente Groq: {e}"
        )


# Mostra um aviso caso não exista uma chave de API
if not groq_api_key and st.session_state.messages:
    st.warning(
        "Insira sua API Key da Groq na barra lateral "
        "para continuar."
    )


# Campo para o usuário enviar uma pergunta
if prompt := st.chat_input("Qual sua dúvida sobre Python?"):

    # Verifica se o cliente foi inicializado
    if client is None:
        st.warning(
            "Insira uma API Key válida da Groq "
            "na barra lateral para começar."
        )

    else:
        # Salva a pergunta do usuário
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        # Exibe a pergunta no chat
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepara o histórico para enviar à API
        messages_for_api = [
            {"role": "system", "content": CUSTOM_PROMPT}
        ]

        messages_for_api.extend(st.session_state.messages)

        # Gera e exibe a resposta do assistente
        with st.chat_message("assistant"):
            with st.spinner("Analisando sua pergunta..."):

                try:
                    # Envia as mensagens para a API da Groq
                    chat_completion = (
                        client.chat.completions.create(
                            messages=messages_for_api,
                            model="openai/gpt-oss-20b",
                            temperature=0.7,
                            max_tokens=2048,
                        )
                    )

                    # Extrai o texto da resposta
                    dsa_ai_resposta = (
                        chat_completion.choices[0]
                        .message.content
                    )

                    # Verifica se a resposta não está vazia
                    if not dsa_ai_resposta:
                        dsa_ai_resposta = (
                            "Não consegui gerar uma resposta. "
                            "Tente perguntar novamente."
                        )

                    # Exibe a resposta
                    st.markdown(dsa_ai_resposta)

                    # Salva a resposta no histórico
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": dsa_ai_resposta
                        }
                    )

                except Exception as e:
                    st.error(
                        f"Erro ao gerar a resposta: {e}"
                    )


# Rodapé do aplicativo
st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>
            Ajuda Imunes AI Coder - Feito para ajudar os
            imunes ao conhecimento a obter mais conhecimento.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
