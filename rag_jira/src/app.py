"""
Fichier pour configurer et lancer l'application streamlit
"""
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

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


# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Comment puis-je vous aider aujourd'hui ?"}
    ]

if (hf_email == '' or hf_password == ''):
    st.warning("Veuillez saisir vos données d'identification Hugging Face 🤗 !", icon='⚠️')
else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    """
    Génère une réponse à partir d'un prompt utilisateur en utilisant un modèle de langage.

    Cette fonction se connecte à Hugging Face avec les identifiants fournis,
    crée un chatbot et génère une réponse basée sur le prompt utilisateur.

    Args:
        prompt_input (str): Le message ou la question de l'utilisateur.
        email (str): L'adresse e-mail pour se connecter à Hugging Face.
        passwd (str): Le mot de passe pour se connecter à Hugging Face.

    Returns:
        str: La réponse générée par le chatbot.
    """
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)

# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_password)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_email, hf_password)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
