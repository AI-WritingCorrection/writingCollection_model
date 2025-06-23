from fastapi import FastAPI
import easyocr
import uvicorn

from models import Metadata

from utils.image_utils import merge_images
from utils.image_utils import decode_base64_image_list

from utils.font_score_utils import evaluate_character

"""
pip install fastapi
pip install uvicorn[standard]
pip install pillow
pip install easyocr
"""




app = FastAPI()
reader = easyocr.Reader(['ko'])  # 한글 지원


@app.post("/font-score/")
async def upload_images(payload: Metadata):
    results = []  # 각 셀의 결과 저장용
    fail_stage_counter = {}  # 실패 단계별 빈도 카운트
    recognized_texts = {}  # 각 cell_id 별 OCR 결과 저장용


    # 각 글자자에 대해 반복
    for cell_id in payload.cellImages.keys():

        # 0. 데이터 추출
        cell_images = payload.cellImages.get(cell_id)
        if not cell_images:
            continue  # 없으면 건너뜀


        stroke_counts = payload.detailedStrokeCounts.get(cell_id)
        stroke_points = payload.firstAndLastStroke.get(cell_id)
        practice_syllabus = payload.practice_text[int(cell_id)]


        # 1. 이미지 디코딩
        images = decode_base64_image_list(cell_images)

        # 2. 병합
        img_bytes = merge_images(images)

        # 3. OCR
        ocr_results = reader.readtext(img_bytes)

        # 4. OCR 결과 확인
        passed_ocr = False
        recognized_text = None  # 초기화

        for _, text, confidence in ocr_results:
            if not recognized_text:  # 가장 첫번째 결과만 저장
                recognized_text = text
            if text == practice_syllabus and confidence > 0.7:
                passed_ocr = True
                break
        
        recognized_texts[cell_id] = recognized_text  # 저장
        """당장은 ocr 통과했다고 가정하고 진행"""
        """실제로는 위의 코드를 사용하여 OCR을 통과했는지 확인해야 합니다."""
        passed_ocr = True

        # OCR 실패 처리
        if not passed_ocr:
            results.append({"score": 0, "stage": "OCR 실패"})
            fail_stage_counter["OCR 실패"] = fail_stage_counter.get("OCR 실패", 0) + 1
            continue


        # 5. 평가 함수 호출
        score_result = evaluate_character(images, stroke_counts, stroke_points, practice_syllabus)

        results.append({
            "score": score_result["score"],
            "stage": score_result["stage"]
        })

        # 실패 단계 기록
        if score_result["stage"] != "완료":
            fail_stage_counter[score_result["stage"]] = fail_stage_counter.get(score_result["stage"], 0) + 1


    # 평균 계산
    avg_score = sum(r["score"] for r in results) / len(results) if results else 0

    # 가장 많이 실패한 단계 찾기
    most_failed = max(fail_stage_counter.items(), key=lambda x: x[1])[0] if fail_stage_counter else None


    # ✅ 최종 응답
    return {
        "summary": {
            "average_score": avg_score,
            "most_failed_stage": most_failed
        },
        "recognized_texts": recognized_texts  # OCR로 인식된 글자들 추가
    }






if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", reload=True)
