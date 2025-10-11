
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
    """ 글쓰기 연습을 위한 텍스트를 생성하는 함수 (최고 속도 버전) """
    model = genai.GenerativeModel('gemini-flash-lite-latest')
    prompt = f"""
    아래의 모든 조건을 엄격하게 지켜서 글쓰기 연습용 텍스트를 생성해줘.

    1. 형식: '{form}' (문장일 경우 ~다 같이 서술어 형태로 끝나야 함)
    2. 최대 길이: {length}자 (이 길이보다 짧아야 함)
    3. 핵심 조건: '{con}'
    4. 부가 조건: 인사나 설명 같은 말은 모두 제외하고, 생성할 텍스트 결과물만 응답으로 줘.
    5. 부가 조건: , 문장 부호나 특수문자 없이, 오직 한글만 사용해서 생성해줘.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"API 호출 중 에러 발생: {e}")
        return "텍스트를 생성하는 데 실패했습니다."

# API 엔드포인트 정의
@router.post("/generate", summary="글쓰기 연습 텍스트 생성")
async def generate_text_endpoint(request: TextRequest):
    """
    주어진 조건(form, length, con)에 맞는 텍스트를 생성하여 반환합니다.
    """
    generated_text = generate_writing_practice_text(
        form=request.form,
        length=request.length,
        con=request.con
    )
    return {"result": generated_text}