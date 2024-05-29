from openai import OpenAI
import streamlit as st
import time
import os

# API 키 설정
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 업데이트된 Assistant ID
assistant_id = "asst_qr6yYrBcphrf4SN52S2ZdEyM"

# 페이지 설정
st.set_page_config(page_title="GREEN 환경 AI챗봇", page_icon="🌍")
st.title("🌍GREEN 환경 AI챗봇")

st.markdown("""
    <style>
    .stApp {
        background-color: #f9f9f9; /* 밝은 회색 배경 */
        color: #333333; /* 진한 회색 텍스트 */
    }
    .stSidebar {
        background-color: #ffffff; /* 흰색 사이드바 */
        color: #333333; /* 진한 회색 텍스트 */
    }
    .stButton > button {
        background-color: #4CAF50; /* 밝은 녹색 버튼 */
        color: white; /* 흰색 텍스트 */
        border-radius: 10px; /* 둥근 모서리 */
    }
    .stTextInput > div > input {
        background-color: #f0f0f0; /* 밝은 회색 입력 상자 */
        color: #333333; /* 진한 회색 텍스트 */
        border-radius: 10px; /* 둥근 모서리 */
    }
    .stAlert {
        background-color: #ffe4e1; /* 미스트로즈색 알림 */
        color: #333333; /* 진한 회색 텍스트 */
    }
    .stMarkdown {
        background-color: #ffffff; /* 흰색 마크다운 */
        color: #333333; /* 진한 회색 텍스트 */
        border-radius: 10px; /* 둥근 모서리 */
        padding: 10px; /* 패딩 추가 */
    }
    </style>
    """, unsafe_allow_html=True)

# # 사이드바 설정
# with st.sidebar:
#     st.subheader("추천 질문")
#     st.info("배려(덕목)의 뜻은?")
#     st.info("생활속에서 예절을 지키지 않는 상황을 알려줘")
#     st.info("예절에 대해서 설명해줘")
#     st.info("정의의 덕목과 이야기를 들려줘")

# 초기 스레드 생성
if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

thread_id = st.session_state.thread_id

# 초기 메시지 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요, 저는 GREEN 환경 AI 챗봇입니다. 무엇을 도와드릴까요?"}]

# 이모지를 설정하는 함수
def get_avatar(role):
    return "🌏" if role == "user" else "🌿"

# 메시지 출력
for msg in st.session_state.messages:
    avatar = get_avatar(msg["role"])
    st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar=get_avatar("user")).write(prompt)

    response = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=prompt,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    thread_messages = client.beta.threads.messages.list(thread_id)
    msg = thread_messages.data[0].content[0].text.value

    # 어시스턴트의 응답을 한 글자씩 출력
    st.session_state.messages.append({"role": "assistant", "content": msg})
    full_message = ""
    message_placeholder = st.empty()
    for char in msg:
        full_message += char
        message_placeholder.write(f"🌿 {full_message}")
        time.sleep(0.05)  # 출력 속도 조절

