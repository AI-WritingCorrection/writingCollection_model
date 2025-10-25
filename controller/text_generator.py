from fastapi import APIRouter
from dto.generatorDTO import TextRequest
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# API 키 설정
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY 환경 변수를 찾을 수 없습니다.")
genai.configure(api_key=api_key)

# FastAPI 라우터 생성
router = APIRouter()

# Gemini 호출 함수
def generate_writing_practice_text(form: str, length: int, con: str) -> str:
    """ 글쓰기 연습을 위한 텍스트를 생성하는 함수 (다양성 확보 버전) """
    model = genai.GenerativeModel('gemini-flash-latest')

    prompt = f"""
    너는 글쓰기 연습을 위한 텍스트를 생성하는 AI야. 아래 모든 조건을 완벽하게 지켜줘.

    1. 형식: '{form}'
    2. 수량: 오직 한 개의 '{form}'만 생성해줘.
    3. 길이: {length}자 (same length)
    4. 핵심 조건: '{con}' (모든글자가 이 조건을 만족할 필요는 없어, 하지만 최대한 많이 포함시켜줘)
    5. 추가 규칙: 문장 부호나 특수문자 없이 오직 한글로만 작성해.
    6. 출력 형식: 다른 설명, 인사, 줄바꿈 없이, 조건에 맞는 결과물 **딱 하나만** 응답해줘.
    7. 중요: **매번 호출할 때마다 다른, 무작위의 새로운 결과**를 생성해야 해. 절대 이전에 생성한 것과 겹치지 않게 해.
    """

    # temperature 값을 높여서(예: 0.8 ~ 1.0) 더 다양한 답변을 유도
    generation_config = {
        "temperature": 0.9,  # 0.0(결정적) ~ 1.0(최대 무작위성)
        # "top_p": 1, (필요시 조절)
        # "top_k": 1, (필요시 조절)
    }

    try:
        # 3. [수정] generate_content 호출 시 generation_config 전달
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        return response.text.strip()
    except Exception as e:
        print(f"API 호출 중 에러 발생: {e}")
        return "텍스트를 생성하는 데 실패했습니다."

# API 엔드포인트 정의
@router.post("/generate", summary="글쓰기 연습 텍스트 생성")
async def generate_text_endpoint(request: TextRequest):
    """
    주어진 조건에 맞는 글쓰기 연습용 텍스트를 생성하여 반환

    클라이언트로부터 **형식, 길이, 조건**을 JSON으로 받아,
    Gemini AI를 통해 조건에 맞는 텍스트를 생성하도록 요청

    - **Request Body (Input)**:
        - `form (str)`: 생성할 텍스트의 형식 ('단어' 또는 '문장')
        - `length (int)`: 최대 글자 수
        - `con (str)`: 텍스트가 만족해야 할 조건 (단계 별로 구체적으로 기술)")

    - **Returns (Output)**:
        - **성공 시 (200 OK)**: `{"result": "생성된 텍스트"}` 형태의 JSON
    """
    generated_text = generate_writing_practice_text(
        form=request.form,
        length=request.length,
        con=request.con
    )
    return {"result": generated_text}