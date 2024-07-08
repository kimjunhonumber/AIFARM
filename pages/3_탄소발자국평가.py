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
st.set_page_config(page_title="나의 인성 테스트")

# 제목
st.title("나의 인성 테스트")

# 사용자 이름 입력
name = st.text_input("■ 이름을 적으세요", "")

# 설문 문항
st.markdown("## ■ 인성 테스트를 위한 설문입니다. 내가 생각하는 정도를 체크해 보세요")


# 질문 1
question1 = "1_내가 불편하지 않다면 다른 친구들이 하고 싶은 대로 하는 것이 마음이 편하다."
response1 = st.radio(f"1. {question1}", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"])
response1_value = int(response1[0]) if response1 else 0


# 질문 2
question2 = "2_ 나는 타인의 의견을 존중하며, 의견이 다를 때도 공손하게 대한다."
response2 = st.radio(f"2. {question2}", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"])
response2_value = int(response2[0]) if response2 else 0

# 질문 3
question3 = "3_ 나는 내가 옳다고 생각하면 내 입장을 강하게 주장한다."
response3 = st.radio(f"3. {question3}", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"])
response3_value = int(response3[0]) if response3 else 0

# 질문 4
question4 = "4_ 다른 사람과 무언가를 함께 할 때는 갈등이 생길 수밖에 없다."
response4 = st.radio(f"4. {question4}", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"])
response4_value = int(response4[0]) if response4 else 0

# 질문 5
question5 = "5_ 나는 다른 친구들의 의견을 들을 때, 새로운 것을 더 배운다."
response5 = st.radio(f"5. {question5}", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"])
response5_value = int(response5[0]) if response5 else 0

# 질문 6
question6 = "6_ 새롭게 해결책을 찾기보다는 내가 해야 할 일에 집중하는 것이 더 낫다."
response6 = st.radio(f"6. {question6}", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"])
response6_value = int(response6[0]) if response6 else 0

# 질문 7
question7 = "7_ 아무도 내 의견에는 흥미가 없다."
response7 = st.radio(f"7. {question7}", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"])
response7_value = int(response7[0]) if response7 else 0

# 질문 8
question8 = "8_ 내가 잘 모를 때에는 잘 아는 친구의 의견을 듣는 것이 좋다."
response8 = st.radio(f"8. {question8}", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"])
response8_value = int(response8[0]) if response8 else 0

# 질문 9
question9 = "9_ 내 의견을 주장하는 것보다 친구들과 사이좋게 잘 지내는 것이 더 중요하다."
response9 = st.radio(f"9. {question9}", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"])
response9_value = int(response9[0]) if response9 else 0

# 질문 10
question10 = "10_ 친구들이 나에게 관심을 두게 하려면 내 의견을 분명히 이야기해야 한다."
response10 = st.radio(f"10. {question10}", ["5 - 매우 그렇다", "4 - 조금 그렇다", "3 - 보통이다", "2 - 별로 그렇지 않다", "1 - 전혀 그렇지 않다"])
response10_value = int(response10[0]) if response10 else 0

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
st.markdown("## ■ 인성 실천 행동을 한 나의 생각과 느낌을 적어 보세요")
thoughts = st.text_area("", "")

@st.cache_data
def analyze_moral_data(name, responses, thoughts, ):
    data = {
        "이름": name,
        "응답": responses,
        "생각과 느낌": thoughts,
    }

    persona = f'''
    이 프롬프트는 사용자로부터 제공된 인성 테스트 데이터를 분석하고 피드백을 제공하는 GPT 모델입니다.
    사용자가 제공한 인성과 관련된 선택 상황, 겪은 상황, 판단, 느낌, 행동 등을 기반으로 인성 피드백을 작성합니다. 양식은 <결과> 인성분석 결과는 종합적으로 결과를 판단해서 최대한 상세하게 이야기 해준다. 점수는 제시하지 않는다. <피드백> 결과에 대한 피드백으로 제공합니다.
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
                {"role": "user", "content": "인성 테스트 데이터에 대한 분석과 피드백을 제공해 주세요."}
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
        st.markdown("## 인성 테스트 결과")
        st.write(analysis)
        
        # 생성된 도덕적 행동 평가서를 TXT 파일로 변환
        txt_file = BytesIO(analysis.encode('utf-8'))
        
        # 다운로드 링크 제공
        st.download_button(
            label="인성적 행동 평가서 다운로드",
            data=txt_file,
            file_name="generated_moral_document.txt",
            mime="text/plain"
        )

