import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
from PIL import Image
import io

# 텍스트를 Markdown 인용문으로 감싸주는 함수
def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 경로 설정 및 API 키 불러오기
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"
with open(secrets_path, "r") as f:
    secrets = toml.load(f)
gemini_api_key1 = secrets["gemini_api_key1"]

# Gemini API 설정
genai.configure(api_key=gemini_api_key1)

# Streamlit 앱 제목
st.title("🌿 식물 진찰기: 건강 상태, 병해충, 종류 판별")

# 이미지 업로드
uploaded_file = st.file_uploader("📷 식물 사진을 업로드 해보세요", type=["jpg", "jpeg", "png"])

# 이미지가 업로드되었을 때
if uploaded_file is not None:
    # 이미지 로딩 및 표시
    img_bytes = uploaded_file.read()
    img = Image.open(io.BytesIO(img_bytes))
    st.image(img, caption="업로드한 식물 사진", use_container_width=True)

    # Gemini 모델 불러오기
    model = genai.GenerativeModel("gemini-1.5-flash")

    # AI에게 요청할 프롬프트
    prompt = '''이 사진 속 식물을 보고 아래 세 가지를 판단해 주세요.

1. 이 식물은 건강하게 자라고 있나요? (좋음/보통/병든 상태로 판단하고 이유 설명)
2. 병해충이 있다면 어떤 종류인지 설명해주세요. 없다면 '병해충 없음'이라고 알려주세요.
3. 이 식물의 종류가 무엇일 가능성이 높은지 AI가 추정해주세요.

설명은 초등학생도 이해할 수 있도록 친절하고 쉽게 말해주세요.'''

    # 분석 요청 및 결과 표시
    with st.spinner("🔍 식물 상태를 분석 중입니다. 잠시만 기다려주세요..."):
        try:
            mime_type = uploaded_file.type
            response = model.generate_content([
                prompt,
                {"inline_data": {"mime_type": mime_type, "data": img_bytes}}
            ])
            response.resolve()

            # 결과 출력
            st.markdown("### 🔍 분석 결과")
            st.markdown(to_markdown(response.text))

        except Exception as e:
            st.error(f"⚠️ 분석 중 오류가 발생했습니다: {e}")
            st.info("다시 시도하거나 다른 이미지를 업로드해보세요.")

else:
    st.info("AI에게 식물을 보여주세요 🌱")


