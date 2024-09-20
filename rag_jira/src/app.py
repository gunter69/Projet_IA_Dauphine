"""
Fichier pour configurer et lancer l'application streamlit
"""
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

from service.indexation import ServiceIndexation

st.set_page_config(page_title="JiraBot 💬🤖")

def reset_conversation():
    """Reset conversation"""
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

with st.sidebar:
    st.title("JiraBot 💬🤖")
    st.header("Your HF login 🤗")
    HUGGINGFACEHUB_API_TOKEN = st.text_input("🔑 API token :", value="", type='password')
    if HUGGINGFACEHUB_API_TOKEN == '':
        st.warning("Please enter your HuggingFace api token!!", icon='⚠️')
    else:
        st.success("Your HuggingFace api token has been taken into account! ", icon='✅')
        ## Configuration LLM
        MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
        llm = HuggingFaceEndpoint(
            repo_id=MODEL,
            max_new_tokens=1024,
            temperature=0.01,
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        )

    st.markdown("***")

    st.markdown(
        "📖 Link to the "
        "[project's Github directory](https://github.com/gunter69/Projet_IA_Dauphine/tree/main/rag_jira)!"
    )

    st.markdown("***")

    st.markdown("**Project :** MongoDB Core Server")
    st.markdown(
        "**Description :** MongoDB Enterprise Server is the commercial edition of MongoDB,"
        " available as part of the MongoDB Enterprise Advanced subscription."
    )

    st.markdown("*This chatbot is there to answer your questions about the project*")
    st.button('Reset Chat', on_click=reset_conversation)

service_indexation = ServiceIndexation()

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

if HUGGINGFACEHUB_API_TOKEN == '':
    st.warning("Please enter your HuggingFace api token!🤗 !", icon='⚠️')
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
    template = """MongoDB Enterprise Server is the commercial edition of MongoDB, available as part of the MongoDB Enterprise Advanced subscription.
You are a conversational assistant solving issues on MongoDB Enterprise Server.
Answer the issue : {prompt_input}
Using the following context between ===.
===
{context}
===
Your answer will be concise and you will explain step by step how to solve this issue."""
    prompt_temp = PromptTemplate.from_template(template)
    print(f"Prompt : {template.format(prompt_input=prompt_input, context=context)}")
    llm_chain = prompt_temp | llm
    return llm_chain.invoke({
            "prompt_input": prompt_input,
            "context": context
        })

# User-provided prompt
if prompt := st.chat_input(placeholder="Your question", disabled=not HUGGINGFACEHUB_API_TOKEN):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    print("Recherche embeddings.")
    documents = service_indexation.entrepot_embeddings.recherche_embeddings(prompt)

    print("Construction contexte.")
    CONTEXTES = ""
    for i, document in enumerate(documents):
        CONTEXTES += f'Issue title : {document.metadata["title"]}\n'
        if i == len(documents)-1:
            CONTEXTES += f'Comments on the issue : \n{document.metadata["comment"]}'
        else:
            CONTEXTES += f'Comments on the issue : \n{document.metadata["comment"]}\n\n'

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("JIRA ticket analysis..."):
            print("Appel au LLM.")
            response = generate_response(prompt, CONTEXTES)
            print("Appel terminé.")
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
