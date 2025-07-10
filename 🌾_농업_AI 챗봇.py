from openai import OpenAI
import streamlit as st
import time
import random
import os


# API 키 설정
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


# 업데이트된 Assistant ID
assistant_id = "asst_0aakRbXEIqJJnO6QVm75yOFZ"

# 페이지 설정
st.set_page_config(page_title="농업 AI 챗봇", page_icon="🍃")
st.title("🍃AI 농업 스마트팜")


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


# 사이드바 설정
with st.sidebar:
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = ""

    thread_btn = st.button("Thread 생성")

    if thread_btn:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        st.subheader(f"Created Thread ID: {st.session_state.thread_id}")
        st.info("스레드가 생성되었습니다.")
        st.info("스레드 ID를 기억하면 대화내용을 이어갈 수 있습니다.")
        st.divider()
        st.subheader("추천 질문")
        st.info("제로 웨이스트를 실천하는 방법은?")
        st.info("탄소 발자국을 줄이는 방법은?")
        st.info("화장품 용기 분리 수거는?")
        st.info("생물종이 다양해야 하는 이유는?")

# 스레드 ID 입력란
thread_id = st.text_input("Thread ID", value=st.session_state.thread_id)

# 초기 메시지 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요, 저는 AI팜 챗봇입니다. 먼저 왼쪽에 있는 'Thread 생성' 버튼을 눌러주시고, 궁금한 점이 있으시면 언제든지 말씀해 주세요. AI가 친절하게 도와드릴게요."}]

# 아이콘을 설정하는 함수
def get_avatar(role):
    return "🐵" if role == "user" else "🐶"

# 메시지 출력
for msg in st.session_state.messages:
    avatar = get_avatar(msg["role"])
    st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input():
    if not thread_id:
        st.error("Please add your thread_id to continue.")
        st.stop()

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
        message_placeholder.write(f"🐶 {full_message}")
        time.sleep(0.05)
