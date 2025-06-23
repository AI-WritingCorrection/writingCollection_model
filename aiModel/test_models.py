from models import Metadata, Offset  # 위에서 정의한 클래스
import base64

sample_data = {
    "user_id": "user123",
    "practice_text": "감자",
    "cellImages": {
        "0": [
            "iVBORw0KGgoAAAANSUhEUgAAA...",  # 실제 테스트할 땐 짧은 문자열로
            "iVBORw0KGgoAAAANSUhEUgAAA..."
        ],
        "1": [
            "iVBORw0KGgoAAAANSUhEUgBBB..."
        ]
    },
    "detailedStrokeCounts": {
        "0": [1, 2, 3],
        "1": [2, 2, 0]
    },
    "firstAndLastStroke": {
        "0": [
            {"x": 20.5, "y": 44.3}, {"x": 34.0, "y": 126.3}
        ],
        "1": [
            {"x": 294.0, "y": 75.3}, {"x": 283.0, "y": 153.3}
        ]
    }
}

# 파싱 테스트
meta = Metadata(**sample_data)

print("✅ Metadata 모델 파싱 성공!")
print(f"사용자 ID: {meta.user_id}")
print(f"연습 텍스트: {meta.practice_text}")
print(f"첫 셀 이미지 수: {len(meta.cellImages['0'])}장")
print(f"첫 번째 셀의 첫 이미지(Base64 일부): {meta.cellImages['0'][0][:30]}...")
print(f"첫 번째 셀의 첫 시작 좌표: {meta.firstAndLastStroke['0'][0]}")
print("세부 획 수:", meta.detailedStrokeCounts)
