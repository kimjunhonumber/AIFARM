from openai import OpenAI
import streamlit as st
import time
import random
from io import BytesIO  # 파일 다운로드를 위해 필요
import os

# API 키 설정
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 페이지 제목 설정
st.set_page_config(page_title="나의 탄소 발자국 평가서")

# CSS 스타일 적용
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #2C3E50;
        margin-bottom: 20px;
    }
    .subtitle {
        text-align: center;
        font-size: 24px;
        color: #2980B9;
        margin-bottom: 40px;
    }
    .question {
        font-size: 18px;
        font-weight: bold;
        color: #34495E;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .radio-label {
        font-size: 16px;
        color: #7F8C8D;
    }
    .result-title {
        font-size: 22px;
        font-weight: bold;
        color: #27AE60;
        margin-top: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# 제목
st.markdown("<div class='main-title'>나의 탄소 발자국 테스트</div>", unsafe_allow_html=True)

# 사용자 이름 입력
name = st.text_input("■ 이름을 적으세요", "")

# 설문 문항
st.markdown("<div class='subtitle'>■ 탄소 발자국 테스트를 위한 설문입니다. 내가 생각하는 정도를 체크해 보세요</div>", unsafe_allow_html=True)

# 질문 1
question1 = "1_나는 일상 생활에서 일회용품 사용을 줄이려고 노력한다."
st.markdown(f"<div class='question'>{question1}</div>", unsafe_allow_html=True)
response1 = st.radio("", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"], index=0)
response1_value = int(response1.split(" - ")[0]) if response1 else 0

# 질문 2
question2 = "2_ 나는 자전거나 대중교통을 자주 이용한다."
st.markdown(f"<div class='question'>{question2}</div>", unsafe_allow_html=True)
response2 = st.radio("", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"], index=0)
response2_value = int(response2.split(" - ")[0]) if response2 else 0

# 질문 3
question3 = "3_ 나는 에너지를 절약하기 위해 집에서 불필요한 전등을 끈다."
st.markdown(f"<div class='question'>{question3}</div>", unsafe_allow_html=True)
response3 = st.radio("", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"], index=0)
response3_value = int(response3.split(" - ")[0]) if response3 else 0

# 질문 4
question4 = "4_ 나는 지역 식품을 구매하여 식품 운송으로 인한 탄소 배출을 줄이려고 한다."
st.markdown(f"<div class='question'>{question4}</div>", unsafe_allow_html=True)
response4 = st.radio("", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"], index=0)
response4_value = int(response4.split(" - ")[0]) if response4 else 0

# 질문 5
question5 = "5_ 나는 재활용을 적극적으로 실천한다."
st.markdown(f"<div class='question'>{question5}</div>", unsafe_allow_html=True)
response5 = st.radio("", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"], index=0)
response5_value = int(response5.split(" - ")[0]) if response5 else 0

# 질문 6
question6 = "6_나는 탄소 배출을 줄이기 위해 채식을 고려하거나 실천하고 있다."
st.markdown(f"<div class='question'>{question6}</div>", unsafe_allow_html=True)
response6 = st.radio("", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"], index=0)
response6_value = int(response6.split(" - ")[0]) if response6 else 0

# 질문 7
question7 = "7_ 나는 물을 절약하기 위해 샤워 시간을 줄인다."
st.markdown(f"<div class='question'>{question7}</div>", unsafe_allow_html=True)
response7 = st.radio("", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"], index=0)
response7_value = int(response7.split(" - ")[0]) if response7 else 0

# 질문 8
question8 = "8_ 나는 전기 자동차나 하이브리드 차량을 이용하려고 한다."
st.markdown(f"<div class='question'>{question8}</div>", unsafe_allow_html=True)
response8 = st.radio("", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"], index=0)
response8_value = int(response8.split(" - ")[0]) if response8 else 0

# 질문 9
question9 = "9_나는 에너지 효율이 높은 가전 제품을 사용한다."
st.markdown(f"<div class='question'>{question9}</div>", unsafe_allow_html=True)
response9 = st.radio("", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"], index=0)
response9_value = int(response9.split(" - ")[0]) if response9 else 0

# 질문 10
question10 = "10_나는 탄소 배출을 줄이기 위해 여행을 자제하거나 가까운 곳으로 간다."
st.markdown(f"<div class='question'>{question10}</div>", unsafe_allow_html=True)
response10 = st.radio("", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"], index=0)
response10_value = int(response10.split(" - ")[0]) if response10 else 0

# 응답 저장
responses = [
    {"question": question1, "response": response1, "value": response1_value},
    {"question": question2, "response": response2, "value": response2_value},
    {"question": question3, "response": response3, "value": response3_value},
    {"question": question4, "response": response4, "value": response4_value},
    {"question": question5, "response": response5, "value": response5_value},
    {"question": question6, "response": response6, "value": response6_value},
    {"question": question7, "response": response7, "value": response7_value},
    {"question": question8, "response": response8, "value": response8_value},
    {"question": question9, "response": response9, "value": response9_value},
    {"question": question10, "response": response10, "value": response10_value}
]

# 인성 실천 행동에 대한 생각과 느낌
st.markdown("## ■ 탄소 발자국 실천 행동을 한 나의 생각과 느낌을 적어 보세요")
thoughts = st.text_area("", "")

@st.cache_data
def analyze_moral_data(name, responses, thoughts):
    data = {
        "이름": name,
        "응답": responses,
        "생각과 느낌": thoughts,
    }

    persona = f'''
    이 프롬프트는 사용자로부터 제공된 탄소 발자국 테스트 데이터를 분석하고 피드백을 제공하는 GPT 모델입니다.
    사용자가 제공한 탄소 발자국과 관련된 선택 상황, 판단, 느낌, 행동 등을 기반으로 탄소 발자국 피드백을 작성합니다. 양식은 <결과> 탄소 발자국 분석 결과는 종합적으로 결과를 판단해서 최대한 상세하게 이야기 해준다. 점수는 제시하지 않는다. <피드백> 결과에 대한 피드백으로 제공합니다.
    다음은 사용자가 제공한 내용입니다:
    이름: {name}
    응답: {responses}
    생각과 느낌: {thoughts}
    '''

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": persona},
                {"role": "user", "content": "탄소 발자국 테스트 데이터에 대한 분석과 피드백을 제공해 주세요."}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"API 요청 중 오류가 발생했습니다: {e}")
        return None

# 결과 분석 및 피드백
if st.button("결과 보기"):
    analysis = analyze_moral_data(name, responses, thoughts)

    if analysis:
        # 분석 결과 출력
        st.markdown("<div class='result-title'>탄소 발자국 테스트 결과</div>", unsafe_allow_html=True)
        st.write(analysis)
        
        # 생성된 도덕적 행동 평가서를 TXT 파일로 변환
        txt_file = BytesIO(analysis.encode('utf-8'))
        
        # 다운로드 링크 제공
        st.download_button(
            label="탄소 발자국 평가서 다운로드",
            data=txt_file,
            file_name="generated_moral_document.txt",
            mime="text/plain"
        )
