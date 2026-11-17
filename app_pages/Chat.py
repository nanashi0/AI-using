import streamlit as st

client = st.session_state["openai_client"]

st.title("Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

def clear():
    st.session_state.messages = []

st.button("Clear", on_click=clear)

# 이전 대화 다시 그리기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.responses.create(
            model="gpt-6-luna",
            input=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
