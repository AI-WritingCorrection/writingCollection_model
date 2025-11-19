# AI손글씨 교정 플랫폼 백엔드/모델
# 아키텍처 구조

# ERD

# 알고리즘 소개

# API 명세서

## 유저 및 인증 (User & Auth)

| Endpoint | Method | Description | Request Body | Response Body |
| --- | --- | --- | --- | --- |
| **/login** | `POST` | Firebase ID 토큰으로 로그인 | `{"id_token": "string"}` | `{"user_id": int, "email": "string", "nickname": "string", ... "jwt": "string"}` |
| **/signup** | `POST` | Firebase ID 토큰 및 사용자 정보로 회원가입 | `id_token: str`, `email: str`, `nickname: str`, `birthdate: datetime`, `provider: AuthProvider`, `profile_pic: file` (form-data) | `{"user_id": int, "email": "string", "nickname": "string", ... "jwt": "string"}` |
| **/logout** | `POST` | 로그아웃 | `Authorization: Bearer <token>` (Header) | `{"message": "Logged out successfully"}` |
| **/getProfile/{user_id}** | `GET` | 사용자 프로필 조회 | | `{"user_id": int, "email": "string", "nickname": "string", ...}` |
| **/updateProfile/{user_id}** | `POST` | 사용자 프로필 정보 업데이트 | `{"nickname": "string", "birthdate": "datetime", "user_type": "UserType"}` | `{"user_id": int, "email": "string", "nickname": "string", ...}` |
| **/uploadProfileImage/{user_id}** | `POST` | 프로필 이미지 업로드 | `file` (form-data) | `{"data": {"profile_pic_url": "string"}}` |
| **/stats/{user_id}** | `GET` | 사용자 통계 조회 | | `[{"mission_id": int, "step_type": "WritingType", "score": float, ...}]` |

## 평가 (Evaluation)

| Endpoint | Method | Description | Request Body | Response Body |
| --- | --- | --- | --- | --- |
| **/evaluate** | `POST` | 손글씨 평가 | `{"user_id": int, "step_id": int, "practice_text": "string", "cell_images": {"cell_id": ["base64_string"]}, "detailed_strokecounts": {"cell_id": [int]}, "firstandlast_stroke": {"cell_id": [{"x": float, "y": float}]}, "user_type": "UserType"}` | `{"avg_score": float, "summary": ["string"], "feedback": [["string"]], "results": [{"original_text": "string", "score": int, ...}]}` |

## 데이터 조회 (Data Retrieval)

| Endpoint | Method | Description | Request Body | Response Body |
| --- | --- | --- | --- | --- |
| **/step** | `GET` | 단계 목록 조회 | | `[{"step_id": int, "step_mission": "string", ...}]` |
| **/practice** | `GET` | 연습 목록 조회 | | `[{"practice_id": int, "practice_text": "string", ...}]` |
| **/missionrecords/{user_id}** | `GET` | 사용자의 미션 기록 조회 | | `[{"step_id": int, "user_id": int, "isCleared": bool}]` |

## 텍스트 생성 (Text Generation)

| Endpoint | Method | Description | Request Body | Response Body |
| --- | --- | --- | --- | --- |
| **/generate** | `POST` | 글쓰기 연습 텍스트 생성 | `{"form": "string", "length": int, "con": "string"}` | `{"result": "생성된 텍스트"}` |
