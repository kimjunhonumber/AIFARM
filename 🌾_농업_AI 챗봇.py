from openai import OpenAI
import streamlit as st
import time
import os

# ───────────────────────────────────────────
# ① 환경 변수 및 클라이언트
# ───────────────────────────────────────────
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

ASSISTANT_ID = "asst_0aakRbXEIqJJnO6QVm75yOFZ"

# ───────────────────────────────────────────
# ② 페이지 & 세션 초기화
# ───────────────────────────────────────────
st.set_page_config(page_title="농업 AI 챗봇", page_icon="🍃")
st.title("🍃AI 농업 스마트팜")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 먼저 왼쪽 ‘Thread 생성’ 버튼을 눌러 새 대화를 시작해주세요 🙂"
        }
    ]
if "thread_id" not in st.session_state:
    st.session_state.thread_id = ""

# ───────────────────────────────────────────
# ③ 사이드바 – Thread 생성
# ───────────────────────────────────────────
with st.sidebar:
    if st.button("Thread 생성"):
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        st.success(f"새 Thread ID가 생성되었습니다:\n{thread.id}")
        st.info("이 ID를 기억하면 이후에도 대화를 이어갈 수 있습니다.")

# ───────────────────────────────────────────
# ④ 사용자가 Thread ID 직접 입력 가능
# ───────────────────────────────────────────
thread_id_input = st.text_input("Thread ID", value=st.session_state.thread_id)
# 사용자가 입력창을 수정했다면 세션 값도 교체
if thread_id_input and thread_id_input != st.session_state.thread_id:
    st.session_state.thread_id = thread_id_input.strip()

current_thread_id = st.session_state.thread_id  # 가독성을 위한 별칭

# ───────────────────────────────────────────
# ⑤ 기존 메시지 출력
# ───────────────────────────────────────────
for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

# ───────────────────────────────────────────
# ⑥ 채팅 입력 & OpenAI 호출
# ───────────────────────────────────────────
if prompt := st.chat_input("메시지를 입력하세요"):
    # 1) Thread ID 확인
    if not current_thread_id:
        st.error("먼저 ‘Thread 생성’ 버튼을 누르거나 Thread ID를 입력해 주세요.")
        st.stop()

    # 2) 사용자 메시지 화면에 출력 + 세션 저장
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # (1) 사용자 메시지를 Thread에 추가
        client.beta.threads.messages.create(
            current_thread_id,
            role="user",
            content=prompt,
        )

        # (2) Assistant 실행
        run = client.beta.threads.runs.create(
            thread_id=current_thread_id,
            assistant_id=ASSISTANT_ID,
        )

        # (3) 실행 상태 폴링
        while run.status not in {"completed", "failed", "expired"}:
            time.sleep(1.5)
            run = client.beta.threads.runs.retrieve(
                thread_id=current_thread_id,
                run_id=run.id,
            )

        if run.status != "completed":
            raise RuntimeError(f"Run 끝 상태가 {run.status}입니다.")

        # (4) 최신 메시지 중 assistant 역할만 추출
        msgs = client.beta.threads.messages.list(current_thread_id).data
        assistant_msgs = [
            c.content[0].text.value
            for c in msgs
            if c.role == "assistant"
        ]
        answer = assistant_msgs[0] if assistant_msgs else "죄송합니다. 답변을 가져오지 못했습니다."

    except Exception as e:
        # NotFoundError 등 모든 예외를 잡아 사용자에게 설명
        st.error(f"⚠️ 오류가 발생했습니다: {e}")
        answer = "오류로 인해 답변을 생성하지 못했습니다. Thread ID를 확인하고 다시 시도해 주세요."

    # 3) 답변을 한 글자씩 출력
    ai_box = st.chat_message("assistant")
    placeholder = ai_box.empty()
    displayed = ""
    for ch in answer:
        displayed += ch
        placeholder.write(displayed)
        time.sleep(0.03)

    # 4) 세션 상태에 저장
    st.session_state.messages.append({"role": "assistant", "content": answer})

