import base64
import streamlit as st

client = st.session_state["openai_client"]

st.title("Home")
st.write("Hello World")  # 실습 2

# 실습 3: 질문 -> gpt-6-luna 응답
@st.cache_data  # 같은 질문이면 API를 다시 부르지 않고 저장된 결과 반환
def ask(_client, question):  # _로 시작하는 인자는 캐시 키에서 제외 (client는 해시 불가)
    response = _client.responses.create(
        model="gpt-6-luna",
        input=question,
    )
    return response.output_text

question = st.text_input("질문을 입력하세요")
if question:
    st.write(ask(client, question))

st.divider()

# 실습 4: 프롬프트 -> 이미지 생성
st.subheader("이미지 생성")
prompt = st.text_input("이미지 프롬프트를 입력하세요")
if st.button("이미지 생성") and prompt:
    with st.spinner("이미지 생성 중... (수십 초 걸릴 수 있음)"):
        img = client.images.generate(
            model="gpt-image-2.6-flare",
            prompt=prompt,
        )
    st.session_state.image_bytes = base64.b64decode(img.data[0].b64_json)

# 마지막으로 생성한 이미지는 다른 입력으로 다시 실행돼도 화면에 남김
if "image_bytes" in st.session_state:
    # 메모리 상의 이미지 보여주기
    st.image(st.session_state.image_bytes)
