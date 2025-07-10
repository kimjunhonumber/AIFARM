import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
from PIL import Image
import io

# Markdown 형식 변환 함수
def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 경로 지정 및 API 키 불러오기
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"
with open(secrets_path, "r") as f:
    secrets = toml.load(f)
gemini_api_key1 = secrets["gemini_api_key1"]

# Gemini 설정
genai.configure(api_key=gemini_api_key1)

# 페이지 UI
st.title("🌿 식물 진찰기: 건강 상태, 병해충, 종류 판별")
uploaded_file = st.file_uploader("📷 식물 사진을 업로드 해보세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 이미지 표시
    img_bytes = uploaded_file.read()
    img = Image.open(io.BytesIO(img_bytes))
    st.image(img, caption="업로드한 식물 사진", use_container_width=True)  # 최신 파라미터 사용

    # 모델 준비
    model = genai.GenerativeModel("gemini-1.5-flash")

    # 프롬프트 정의
    prompt = '''이 사진 속 식물을 보고 아래 세 가지를 판단해 주세요.

1. 이

