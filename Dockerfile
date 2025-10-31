# 공식 파이썬 런타임을 부모 이미지로 사용합니다.
FROM python:3.10-slim

# 컨테이너의 작업 디렉토리를 설정합니다.
WORKDIR /app

# 요구사항 파일을 복사하고 종속성을 설치합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 애플리케이션 코드를 복사합니다.
COPY . .

# 앱이 실행되는 포트를 노출합니다.
EXPOSE 8000

# entrypoint.sh 스크립트에 실행 권한 부여
RUN chmod +x entrypoint.sh

# 컨테이너 시작 시 entrypoint.sh를 실행하도록 설정
ENTRYPOINT ["./entrypoint.sh"]

# 애플리케이션을 실행하는 명령어입니다.
CMD ["gunicorn", "main:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "-w", "1", \
     "-b", "0.0.0.0:8000", \
     "--preload"]