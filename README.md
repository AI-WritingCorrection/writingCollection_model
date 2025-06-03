# AI손글씨 교정 플랫폼 백엔드/모델
# 아키텍처 구조

# 실습 환경 구축
리포지토리를 클론한 사용자는 다음 단계를 따라야 합니다. (아래 예시는 일반적인 venv 사용 기준)
## 1.리포지토리 클론

## 2.가상환경 생성
프로젝트 루트(즉, requirements.txt가 있는 디렉토리)에서<p>
```python3 -m venv venv```
<p>(여기서 venv라는 이름은 관례일 뿐이니, 다른 이름(예: env)을 써도 상관없습니다.)

### 3.가상환경 활성화
-macOS/Linux(bash/zsh)
```source venv/bin/activate```

-Windows(cmd.exe)
```venv\Scripts\activate```

-Windows(Powershell)
```.\venv\Scripts\Activate.ps1```

### 4.의존성 설치
```pip install --upgrade pip```<p>
```pip install -r requirements.txt```

### 5.서버 실행 확인
```uvicorn main:app --reload```

• main:app 부분은 실제 FastAPI 애플리케이션이 정의된 모듈 경로에 맞춰 변경할 수 있습니다.<p>
• 실행 후 터미널에 아래와 유사한 메시지가 출력되면 정상적으로 서버가 구동된 것입니다.<p>
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

### 6.requirements.txt 업데이트 방법
로컬에서 새로운 패키지를 설치한 후, requirements.txt를 갱신하려면:
```pip freeze > requirements.txt```

• 만약 Windows PowerShell에서 스크립트 실행 정책 때문에 Activate.ps1이 거부될 경우,<p> 
관리자 권한으로 PowerShell을 실행한 뒤 아래 명령을 입력하여 임시로 실행 정책을 풀어줄 수 있습니다.
```Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass```

### 7. 가상환경 비활성화
작업이 끝난 뒤 가상환경을 빠져나오려면:
```deactivate```
