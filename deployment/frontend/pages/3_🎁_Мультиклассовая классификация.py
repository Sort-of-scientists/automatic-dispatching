import time
import streamlit as st
import pandas as pd

from src.utils import *
from src.constants import *

st.set_page_config(
    page_icon="🎁",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("# Мультикласс")
st.markdown(
    """
    Как мы и сказали ранее, мы предлагаем чуть-чуть изменить постановку задачи!
    Теперь для каждого обращения может быть не только одна **Точка отказа**, а сразу несколько!\n
    Как и в интерфейсе пользователя, вам предлагается ввести тему и описание обращения.
    После нажатия на кнопку перед вами появятся полоски уверенности, говорящие сами за себя :)
    """
)

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



theme = st.text_input(label="Тема", value="Проблема с камерой")

description = st.text_area(
    label="Описание",
    height=300,
    value="Добрый день! Камера не включается, операционная система зависает при запуске приложений."
)

button = st.button("Отправить обращение", use_container_width=True)


if button:
    predictions = send_request_to_multilabel_model(theme + " [SEP] " + description)

    if len(predictions) > 0:
        for pred in predictions:
            label = pred["label"]
            score = pred["score"]
            
            col1, col2 = st.columns([1, 3])

            with col1:
                st.markdown(f"**{label}**")

            with col2:
                score_percentage = score * 100
                color = "green" if score > 0.8 else "orange" if score > 0.5 else "red"
                
                st.markdown(f"""
                    <div style="background-color:#d3d3d3; width:100%; border-radius:5px; padding:5px;">
                        <div style="width:{score_percentage}%; background-color:{color}; height:20px; border-radius:5px;">
                        </div>
                    </div>
                    <p style="text-align:center;">{score:.0%}</p>
                    """, unsafe_allow_html=True)
                
    else:
        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown(f"**Консультация**")

        with col2:
            score_percentage = 100
            color = "green"
            
            st.markdown(f"""
                <div style="background-color:#d3d3d3; width:100%; border-radius:5px; padding:5px;">
                    <div style="width:{score_percentage}%; background-color:{color}; height:20px; border-radius:5px;">
                    </div>
                </div>
                <p style="text-align:center;">{1.0:.0%}</p>
                """, unsafe_allow_html=True)