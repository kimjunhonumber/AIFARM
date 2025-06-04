
import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
from PIL import Image
import io
import base64

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# Gemini API 키 설정
gemini_api_key1 = secrets["gemini_api_key1"]
genai.configure(api_key=gemini_api_key1)

# 페이지 구성
st.title("🌿 식물 진찰기: 건강 상태, 병해충, 종류 판별")
uploaded_file = st.file_uploader("📷 식물 사진을 업로드 해보세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 이미지 로딩 및 표시
    img_bytes = uploaded_file.read()
    img = Image.open(io.BytesIO(img_bytes))
    st.image(img, caption="업로드한 식물 사진", use_column_width=True)

    # 이미지 Base64 인코딩 처리
    base64_img = base64.b64encode(img_bytes).decode("utf-8")

    # 모델 불러오기
    model = genai.GenerativeModel("gemini-pro-vision")

    # 프롬프트
    prompt = '''이 사진 속 식물을 보고 아래 세 가지를 판단해 주세요.

1. 이 식물은 건강하게 자라고 있나요? (좋음/보통/병든 상태로 판단하고 이유 설명)
2. 병해충이 있다면 어떤 종류인지 설명해주세요. 없다면 '병해충 없음'이라고 알려주세요.
3. 이 식물의 종류가 무엇일 가능성이 높은지 AI가 추정해주세요.

설명은 초등학생도 이해할 수 있도록 친절하고 쉽게 말해주세요.'''

    # 요청 전송
    response = model.generate_content([
        {"text": prompt},
        {"inline_data": {"mime_type": "image/png", "data": img_bytes}}
    ])

    response.resolve()
    st.markdown("### 🔍 분석 결과")
    st.markdown(to_markdown(response.text))

else:
    st.info("AI에게 식물을 보여주세요 🌱")
