import openai
import streamlit as st
import time
import random
from io import BytesIO  # 파일 다운로드를 위해 필요
import os

# API 키 설정
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
openai.api_key = os.environ["OPENAI_API_KEY"]

st.set_page_config(layout="wide")

st.title("🌿 환경 습관 평가")

# 사용자로부터 필요한 정보를 입력받습니다.
st.header("환경 습관 체크리스트")
st.write("각 항목에 대해 해당하는 옵션을 선택하세요.")

plastic_usage = st.radio("일회용 플라스틱 사용을 얼마나 자제하고 있나요?", ["항상 그렇다", "자주 그렇다", "가끔 그렇다", "거의 안 그렇다", "전혀 안 그렇다"])
recycling = st.radio("재활용을 얼마나 생활화하고 있나요?", ["항상 그렇다", "자주 그렇다", "가끔 그렇다", "거의 안 그렇다", "전혀 안 그렇다"])
energy_saving = st.radio("에너지를 절약하기 위해 어떤 노력을 하고 있나요?", ["항상 그렇다", "자주 그렇다", "가끔 그렇다", "거의 안 그렇다", "전혀 안 그렇다"])
water_saving = st.radio("물 절약을 위해 어떤 노력을 하고 있나요?", ["항상 그렇다", "자주 그렇다", "가끔 그렇다", "거의 안 그렇다", "전혀 안 그렇다"])
public_transport = st.radio("대중교통을 얼마나 자주 이용하나요?", ["항상 그렇다", "자주 그렇다", "가끔 그렇다", "거의 안 그렇다", "전혀 안 그렇다"])

st.divider()

@st.cache_data  # st.experimental_memo 대신 st.cache_data 사용
def generate_environmental_feedback(plastic_usage, recycling, energy_saving, water_saving, public_transport):
    persona = f'''
    이 프롬프트는 사용자로부터 제공된 환경 습관에 대한 정보를 바탕으로, 사용자의 환경 보호 습관을 평가하고 개선할 수 있는 구체적인 방안을 제시합니다. 
    사용자가 제공한 내용이 현실에 맞지 않거나 사실에 맞지 않는 경우 GPT가 수정해서 작성합니다. 환경 습관에 대한 평가와 피드백은 첫째, 둘째, 셋째 형식으로 개조식으로 작성합니다.
    다음은 사용자가 제공한 내용입니다.
    일회용 플라스틱 사용: {plastic_usage}
    재활용 습관: {recycling}
    에너지 절약: {energy_saving}
    물 절약: {water_saving}
    대중교통 이용: {public_transport}
    GPT는 이 정보를 바탕으로 환경 보호 습관에 대해 첫째, 둘째, 셋째 형식으로 피드백을 제공해 주세요.
    '''

    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": persona},
            {"role": "user", "content": "환경 습관에 대해서 평가해 주세요"}
        ],
        max_tokens=3000,
        temperature=0.7
    )
    return response.choices[0].message.content

# 환경 습관 평가 버튼
if st.button("환경 습관 평가"):
    environmental_feedback = generate_environmental_feedback(plastic_usage, recycling, energy_saving, water_saving, public_transport)
    st.subheader("환경 습관 평가 및 피드백")
    st.write(environmental_feedback)
    
    # 생성된 피드백을 TXT 파일로 변환
    txt_file = BytesIO(environmental_feedback.encode('utf-8'))
    
    # 다운로드 링크 제공
    st.download_button(
        label="환경 습관 평가서 다운로드",
        data=txt_file,
        file_name="environmental_feedback.txt",
        mime="text/plain"
    )

