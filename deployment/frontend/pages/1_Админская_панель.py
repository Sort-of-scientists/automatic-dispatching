import streamlit as st
import pandas as pd

from src.utils import get_messages
from src.constants import LABELS, THRESHOLDS

# Page title
st.markdown("# Админская панель")


st.markdown("✅ - достаточно информации по обращению")
st.markdown("❌ - мало информации по обращению")

# Selection boxes
col1, col2 = st.columns(2)

with col1:
    equipment = st.selectbox(label="Тип устройства", options=["Все"] + LABELS["equipment"])

with col2:
    failure = st.selectbox(label="Точка отказа", options=["Все"] + LABELS["failure"])

# Display ticket list title
st.markdown("## Список обращений")

# Display messages if equipment or failure is selected
if equipment or failure:
    messages = get_messages(equipment, failure)

    for message in messages:
        
        if message["failure_score"] >= THRESHOLDS["failure"] and message["equipment_score"] >= THRESHOLDS["equipment"]:
            with st.expander(f"{message['equipment']} - {message['failure']}", icon="✅"):
                st.markdown(
                    f"""
                    **Устройство**: {message['equipment']}  
                    **Точка отказа**: {message['failure']}  
                    **Сообщение**: {message['text']}
                    """
                )

        else:
            with st.expander(f"{message['equipment']} - {message['failure']}", icon="❌"):
                st.markdown(
                    f"""
                    **Устройство**: {message['equipment']}  
                    **Точка отказа**: {message['failure']}  
                    **Сообщение**: {message['text']}
                    """
                )
