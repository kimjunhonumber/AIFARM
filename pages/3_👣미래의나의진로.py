
from openai import OpenAI
import streamlit as st
import os
from io import BytesIO

# API 키 설정
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 페이지 제목 설정
st.set_page_config(page_title="미래 AI 진로 탐색")

# CSS 스타일
st.markdown("""
    <style>
        .title {font-size: 36px; font-weight: bold; text-align: center; color: #4CAF50; margin-top: 20px;}
        .subtitle {font-size: 24px; font-weight: bold; text-align: center; color: #555; margin-bottom: 20px;}
        .result-title {font-size: 24px; font-weight: bold; color: #FF5722; margin-top: 20px;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🧠 나의 AI 진로 탐색 테스트</div>", unsafe_allow_html=True)

name = st.text_input("■ 이름을 적으세요", "")

st.markdown("<div class='subtitle'>■ 아래 질문에 답하며, AI와 기술에 대한 나의 생각을 확인해 보세요.</div>", unsafe_allow_html=True)

questions = [
    "1_ 나는 새로운 기술(AI, 앱 등)을 배우는 것이 흥미롭다.",
    "2_ 나는 문제를 해결할 때 기술을 활용하려고 노력한다.",
    "3_ 나는 친구들과 협업해서 디지털 도구를 잘 활용한다.",
    "4_ 나는 AI가 세상을 바꾸고 있다고 느낀다.",
    "5_ 나는 AI와 관련된 직업에 관심이 있다.",
    "6_ 나는 데이터를 읽고 이해하는 데 관심이 있다.",
    "7_ 나는 스마트기기나 로봇을 다루는 것이 재미있다.",
    "8_ 나는 나만의 앱이나 프로그램을 만들어보고 싶다.",
    "9_ 나는 사회 문제를 AI로 해결할 수 있을까 고민해본 적이 있다.",
    "10_ 나는 미래에 어떤 기술이 필요할지 생각해본 적이 있다."
]

responses = []
for i, q in enumerate(questions):
    key = f"q{i+1}"
    r = st.radio(f"{i+1}. {q}", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"], key=key)
    responses.append({"question": q, "response": r, "value": int(r[0]) if r else 0})

st.markdown("<div class='subtitle'>■AI와 기술에 대해 느낀 점이나 꿈을 자유롭게 적어 보세요</div>", unsafe_allow_html=True)
thoughts = st.text_area("", "", key="thoughts")

@st.cache_data
def analyze_ai_profile(name, responses, thoughts):
    prompt = f'''
이 프롬프트는 초등학생의 AI 역량과 기술 적응력, 창의적 문제 해결 태도를 분석하고 그에 맞는 미래형 직업을 추천하는 GPT입니다.
학생이 응답한 내용을 바탕으로 다음 두 가지를 작성해주세요:

<결과>
학생의 AI 적응력, 창의성, 협업, 문제해결력 등을 분석하여 특성을 종합적으로 설명해주세요.

<추천 직업>
학생의 특성과 응답을 바탕으로 어울리는 미래형 직업 3가지를 추천하고, 그 이유를 간단히 덧붙여주세요.

입력된 정보는 다음과 같습니다:
이름: {name}
응답: {responses}
생각과 느낌: {thoughts}
'''

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "이 학생의 미래 AI 진로 분석 결과를 작성해주세요."}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"GPT 요청 중 오류가 발생했습니다: {e}")
        return None

if st.button("결과 보기"):
    analysis = analyze_ai_profile(name, responses, thoughts)
    if analysis:
        st.markdown("<div class='result-title'>📄 AI 진로 분석 결과</div>", unsafe_allow_html=True)
        st.write(analysis)
        txt_file = BytesIO(analysis.encode('utf-8'))
        st.download_button(
            label="AI 진로 리포트 다운로드",
            data=txt_file,
            file_name="AI_진로_리포트.txt",
            mime="text/plain"
        )
