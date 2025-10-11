from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import controller.evaluation  as evaluate
import controller.auth as auth
import controller.get_fromDB as loadData
import controller.userController as loadUser
import controller.text_generator as text_generator

#http://127.0.0.1:8000/docs
app = FastAPI(title="AI-HandWriting-Evaluation")
app.include_router(evaluate.router, prefix="/api/step", tags=["Evaluation"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(loadData.router, prefix="/api/data", tags=["Data"])
app.include_router(loadUser.router, prefix="/api/user", tags=["User"])
app.include_router(text_generator.router, prefix="/api/text", tags=["TextGenerator"])

# 허용할 출처(Origin) 목록을 정의합니다. 
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://10.0.2.2:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "http://52.78.166.204:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Flutter 또는 웹뷰가 접근할 도메인/포트
    allow_credentials=True,
    allow_methods=["*"],              # GET, POST 등 모든 메서드 허용
    allow_headers=["*"],              # 헤더 허용
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)