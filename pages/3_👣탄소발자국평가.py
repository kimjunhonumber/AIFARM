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
st.markdown("<div class='main-title'>🌍 나의 탄소 발자국 테스트 🌿</div>", unsafe_allow_html=True)

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
response6 = st.radio("", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 -
