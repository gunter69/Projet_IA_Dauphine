"""
Fichier pour configurer et lancer l'application streamlit
"""
import os
import streamlit as st
from dotenv import load_dotenv
# from hugchat import hugchat
# from hugchat.login import Login
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

from service.indexation import ServiceIndexation

load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(
    repo_id=MODEL,
    max_length=128,
    temperature=0.5,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
)

# Titre de l'application
st.set_page_config(page_title="JiraBot 💬🤖")

# Hugging Face Credentials
with st.sidebar:
    st.title("JiraBot 💬🤖")
    st.header("Vos identifiants HF 🤗")
    hf_email = st.text_input("📧 Email :", value="", type="default")
    hf_password = st.text_input("🔑 Mot de passe :", value="", type='password')
    if (hf_email == '' or hf_password == ''):
        st.warning("Veuillez saisir vos données d'identification !", icon='⚠️')
    else:
        st.success("Vos données d'identification ont été pris en compte ! ", icon='✅')

    st.markdown(
        '📖 Learn how to build this app in this '
        '[blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!'
    )

## Indexation
service_indexation = ServiceIndexation()
entrepot_issues = service_indexation.collecter_les_issues("xp/jira_issues_2.csv")
entrepot_embeddings = service_indexation.stocker_les_documents_dans_vector_store(entrepot_issues)

## Historique des messages
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Comment puis-je vous aider aujourd'hui ?"}
    ]

## Connexion Hugging Face
if (hf_email == '' or hf_password == ''):
    st.warning("Veuillez saisir vos données d'identification Hugging Face 🤗 !", icon='⚠️')
else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input, context):
    """
    Génère une réponse à partir d'un prompt utilisateur en utilisant un modèle de langage.
    """
    template = """Répond à la question suivante : {prompt_input} en t'aidant du contexte suivant : {context}"""
    prompt_temp = PromptTemplate.from_template(template)
    llm_chain = prompt_temp | llm
    return llm_chain.invoke({
            "prompt_input": prompt_input,
            "context": context
        })

# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_password)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    documents = entrepot_embeddings.recherche_embeddings(prompt)

    print(documents)

    CONTEXTES = ""
    for document in documents:
        CONTEXTES += document.metadata["comment"]
        CONTEXTES += "\n\n"

    print("DEBUG", CONTEXTES)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, CONTEXTES)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
