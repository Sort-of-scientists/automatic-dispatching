import time
import streamlit as st

from src.utils import *
from src.constants import *


st.set_page_config(page_title="Пользовательская панель", page_icon="📈")

st.markdown("# Пользовательская панель")

st.markdown(
    """
    <style>
    .stTextArea textarea {
        resize: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

theme = st.text_input(label="Тема")

description = st.text_area(
    label="Описание",
    height=300
)

if st.button("Отправить обращение", use_container_width=True):
    response = send_request_to_models_backend(theme + " [SEP] " + description)

    if response["numbers"]["score"] < THRESHOLDS["numbers"]:
        alert = st.error("Введите серийный номер устройства!")

    else:
        insert_message_to_database(
            text=theme + "\n" + description,
            failure=response["failure"]["label"],
            failure_score=float(response["failure"]["score"]),
            equipment=response["equipment"]["label"],
            equipment_score=float(response["equipment"]["score"]),
            number=response["numbers"]["label"]
        )
    
    alert = st.success("Обращение отправлено!")

    time.sleep(ALERT_DELAY)

    alert.empty()

