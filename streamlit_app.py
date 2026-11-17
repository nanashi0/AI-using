import streamlit as st
from openai import OpenAI

# 진입 파일: 사이드바와 페이지 목록만 담당
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password")
if api_key:
    st.session_state["openai_client"] = OpenAI(api_key=api_key)

pg = st.navigation([
    st.Page("app_pages/Home.py", title="Home", icon=":material/home:"),
    st.Page("app_pages/Chat.py", title="Chat", icon=":material/chat:"),
    st.Page("app_pages/Chatbot.py", title="Chatbot", icon=":material/local_library:"),
    st.Page("app_pages/ChatPDF.py", title="ChatPDF", icon=":material/picture_as_pdf:"),
])

# 키가 없으면 어느 페이지든 안내만 띄우고 멈춤
if "openai_client" not in st.session_state:
    st.info("사이드바에 OpenAI API Key를 입력하세요.")
    st.stop()

pg.run()
