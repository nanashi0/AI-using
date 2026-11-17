import streamlit as st

client = st.session_state["openai_client"]

st.title("ChatPDF")

# 업로드 화면: vector store가 없을 때만 보임
if "vector_store_id" not in st.session_state:
    uploaded = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
    if uploaded is None:
        st.stop()
    with st.spinner("PDF를 읽는 중..."):
        vector_store = client.vector_stores.create(name=uploaded.name)
        vs_file = client.vector_stores.files.upload_and_poll(
            vector_store_id=vector_store.id,
            file=(uploaded.name, uploaded.getvalue()),
        )
    # 다시 실행돼도 vector store를 또 만들지 않도록 저장
    st.session_state.vector_store_id = vector_store.id
    st.session_state.pdf_file_id = vs_file.id
    st.session_state.pdf_name = uploaded.name
    st.session_state.pdf_messages = []
    st.rerun()

def clear():
    st.session_state.pdf_messages = []

def leave():
    client.vector_stores.delete(st.session_state.vector_store_id)
    client.files.delete(st.session_state.pdf_file_id)
    for key in ["vector_store_id", "pdf_file_id", "pdf_name", "pdf_messages"]:
        del st.session_state[key]

st.caption(f"📄 {st.session_state.pdf_name}")
col1, col2 = st.columns(2)
col1.button("Clear", on_click=clear, use_container_width=True)
col2.button("Leave", on_click=leave, use_container_width=True)

for message in st.session_state.pdf_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("PDF 내용에 대해 질문하세요"):
    st.session_state.pdf_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.responses.create(
            model="gpt-6-luna",
            input=st.session_state.pdf_messages,
            tools=[{
                "type": "file_search",
                "vector_store_ids": [st.session_state.vector_store_id],
            }],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.pdf_messages.append({"role": "assistant", "content": response})
