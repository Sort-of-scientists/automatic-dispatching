import time
import streamlit as st

from src.utils import send_request_to_backend
from src.constants import *

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

st.header("Поддержка")

#equipment_warning = st.warning("Недостаточно информации о типе устройства. Пожалуйста, уточните свое сообщение!")
#failure_warning = st.warning("Недостаточно информации о точке отказа. Пожалуйста, уточните свое сообщение!")

#error = st.error("Введите серийный номер устройства!")

theme = st.text_input(label="Тема")

description = st.text_area(
    label="Описание",
    height=300
)

if st.button("Отправить обращение", use_container_width=True):
    response = send_request_to_backend(theme + "[SEP]" + description)

    if response["numbers"]["score"] < THRESHOLDS["numbers"]:
        alert = st.error("Введите серийный номер устройства!")

    else:
        if response["failure"]["score"] < THRESHOLDS["failure"] and response["equipment"]["score"] >= THRESHOLDS["equipment"]:
            alert = st.warning("Недостаточно информации о точке отказа. Пожалуйста, уточните свое сообщение!")

        if response["equipment"]["score"] < THRESHOLDS["equipment"] and response["failure"]["score"] >= THRESHOLDS["failure"]:
            alert = st.warning("Недостаточно информации о типе устройства. Пожалуйста, уточните свое сообщение!")

        if response["equipment"]["score"] < THRESHOLDS["equipment"] and response["failure"]["score"] < THRESHOLDS["failure"]:
            alert = st.warning("Недостаточно информации о точке отказа и типе устройства. Пожалуйста, уточните свое сообщение!")
    
        else:
            alert = st.success("Обращение отправлено!")
    
    time.sleep(3)

    alert.empty()

