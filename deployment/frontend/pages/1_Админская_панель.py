import streamlit as st
import pandas as pd

from src.utils import list_numbers, get_message_by_number, get_messages
from src.constants import LABELS

st.markdown("# Админская панель")

col1, col2 = st.columns(2)

with col1:
    equipment = st.selectbox(label="Тип устройства", options=LABELS["equipment"])

with col2:
    failure = st.selectbox(label="Точка отказа", options=LABELS["failure"])


st.markdown("## Список тикетов")

if equipment or failure:
    messages = get_messages(equipment, failure)

    for message in messages:
    
        with st.container(border=10):

            st.markdown(
                f"""
                ### **{message["equipment"]}**\n #### **{message["failure"]}**\n {message["text"]}
                """
            )

