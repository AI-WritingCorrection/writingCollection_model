from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#http://127.0.0.1:8000/docs
app = FastAPI()

# 허용할 출처(Origin) 목록을 정의합니다. 
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://10.0.2.2:3000",
    "http://localhost:8000",
    # 필요 시 추가
    "*",  # 개발 중에는 모든 출처를 허용할 수도 있지만, 운영환경에선 최대한 제한할 것
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Flutter 또는 웹뷰가 접근할 도메인/포트
    allow_credentials=True,
    allow_methods=["*"],              # GET, POST 등 모든 메서드 허용
    allow_headers=["*"],              # 헤더 허용
)
@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}