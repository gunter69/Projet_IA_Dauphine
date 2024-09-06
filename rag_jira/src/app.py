"""
Fichier pour configurer et lancer l'application streamlit
"""
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

from service.indexation import ServiceIndexation


st.set_page_config(page_title="JiraBot 💬🤖")

with st.sidebar:
    st.title("JiraBot 💬🤖")
    st.header("Vos identifiants HF 🤗")
    HUGGINGFACEHUB_API_TOKEN = st.text_input("🔑 Token d'API :", value="", type='password')
    if HUGGINGFACEHUB_API_TOKEN == '':
        st.warning("Veuillez saisir votre token d'api HuggingFace !", icon='⚠️')
    else:
        st.success("Votre token d'api HuggingFace a été pris en compte ! ", icon='✅')
        ## Configuration LLM
        MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
        llm = HuggingFaceEndpoint(
            repo_id=MODEL,
            max_length=128,
            temperature=0.5,
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        )

    st.markdown(
        '📖 Lien vers le répertoire '
        '[Github du projet](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!'
    )

service_indexation = ServiceIndexation()

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Comment puis-je vous aider aujourd'hui ?"}
    ]

if HUGGINGFACEHUB_API_TOKEN == '':
    st.warning("Veuillez saisir votre token d'api HuggingFace 🤗 !", icon='⚠️')
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def generate_response(prompt_input, context):
    """
    Génère une réponse à partir d'un prompt utilisateur en utilisant un modèle de langage.
    """
#     template = """Tu es un assistant conversationnel qui répond en français.
# Tu dois répondre à la question : {prompt_input}
# Pour répondre tu dois t'aider du contexte suivant : {context}"""
    template = """Tu es un assistant conversationnel.
Tu dois répondre à la question : {prompt_input}
Pour répondre tu dois t'aider du contexte suivant : {context}"""
    prompt_temp = PromptTemplate.from_template(template)
    llm_chain = prompt_temp | llm
    return llm_chain.invoke({
            "prompt_input": prompt_input,
            "context": context
        })

# User-provided prompt
if prompt := st.chat_input(placeholder="Votre question", disabled=not HUGGINGFACEHUB_API_TOKEN):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    documents = service_indexation.entrepot_embeddings.recherche_embeddings(prompt)

    CONTEXTES = ""
    for document in documents:
        CONTEXTES += document.metadata["comment"]
        CONTEXTES += "\n\n"

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Analyse des tickets JIRA..."):
            response = generate_response(prompt, CONTEXTES)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
