import openai
import streamlit as st
import os

# API 키 설정
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
openai.api_key = os.environ["OPENAI_API_KEY"]

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

st.title("🌿💭 환경동화 이미지 🌟🌍")

# 문제상황 입력
presentation_text = st.text_area("📖📝 환경 스토리를 입력해 주세요.", height=300)

# 이미지 스타일 선택
image_style = st.selectbox("🖌️🎨 이미지 스타일 선택", ["🌅 사실적", "🎨 미니멀 일러스트레이션", "📚 만화적", "📰 웹툰"])

# 이미지 생성 버튼
generate_button = st.button("✨🖼️ 이미지 생성 ✨")

if generate_button and presentation_text:
    # 선택한 스타일에 따라 프롬프트 수정
    style_prompt = {
        "🌅 사실적": "사실적인 스타일로",
        "🎨 미니멀 일러스트레이션": "미니멀 일러스트레이션 스타일로",
        "📚 만화적": "만화적 스타일로",
        "📰 웹툰": "교과서에 나오는 삽화 스타일로, 한국 도덕 초등학교 교과서 스타일로"
    }

    prompt = f"{presentation_text} {style_prompt[image_style]}"

    try:
        # OpenAI API를 호출하여 이미지 생성
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        # 생성된 이미지 표시
        generated_image_url = response['data'][0]['url']
        st.image(generated_image_url, caption="🖼️ 나의 문제상황 🌿")

        # 이미지 다운로드 버튼 생성
        st.markdown(f"[📥 이미지 다운로드]({generated_image_url})", unsafe_allow_html=True)
    except Exception as e:
        st.error("🚨 이미지 생성 중 오류 발생: " + str(e))
