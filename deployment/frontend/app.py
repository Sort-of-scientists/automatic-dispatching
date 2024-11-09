import streamlit as st

from src.utils import make_request

CHAT_ANSWER_TEMPLATE = \
"""
**Тип оборудования**: {0}\n
**Точка отказа**: {1}\n
**Cерийный номер**: {2}\n
\n
**Рекомендация**: Выкиньте этот кусок говна! :)))
"""

st.title("СИЛА-Бот")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Я СИЛА Бот. Опишите свою проблему и я помогу решить ее!"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = make_request(prompt)
    
    if len(response["number"]) == 0:
        response = \
            """
            К сожалению, я ничем не могу помочь! Пожалуйста, введите серийный номер устройства!
            """

    else:
        response = CHAT_ANSWER_TEMPLATE.format(
            response["equipment"], 
            response["failure"], 
            response["number"]
        )
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})