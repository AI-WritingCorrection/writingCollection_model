from fastapi import APIRouter, Depends
from database import get_db
from dto.resultDTO import ResultCreate, ResultResponse
from service.missionRecordService import clear_mission_record, create_mission_record
from service.resultService import create_result
from aiModel.utils.image_utils import merge_images
from aiModel.utils.image_utils import decode_base64_image_list
from aiModel.utils.font_score_utils import evaluate_character
from sqlalchemy.orm import Session

from service.userService import get_user_by_id

router=APIRouter()

reader = None  # will be initialized lazily

@router.post("/evaluate", response_model=ResultResponse)
async def evaluate_handwriting(payload: ResultCreate,  db: Session = Depends(get_db)):
    global reader
    if reader is None:
        import easyocr
        reader = easyocr.Reader(
            ['ko'],
            gpu=False,                     # GPU 대신 CPU만 사용
            model_storage_directory='/home/ec2-user/.easyocr_cache',   # 모델 캐시 경로 변경
            download_enabled=True,        # 불필요한 다운로드 방지
            verbose=False                  # 로깅 최소화
        )
    current_user=get_user_by_id(db=db, user_id=payload.user_id)
    if not current_user:
        return {"error": "User not found"}, 404

    #1)Mission Record 생성
    mission_record=create_mission_record(db, payload)
    
    #2)모델 채점
    results = []  # 각 셀의 결과 저장용
    fail_stage_counter = {}  # 실패 단계별 빈도 카운트
    recognized_texts = {}  # 각 cell_id 별 OCR 결과 저장용


    # 각 글자자에 대해 반복
    for cell_id in payload.cell_images.keys():
        # 0. 데이터 추출
        cell_images = payload.cell_images.get(cell_id)
        if not cell_images:
            continue  # 없으면 건너뜀


        stroke_counts = payload.detailed_strokecounts.get(cell_id)
        stroke_points = payload.firstandlast_stroke.get(cell_id)
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
            print(f"Cell {cell_id} OCR 결과: {text} (신뢰도: {confidence})")  # 디버깅용 출력
            if not recognized_text:  # 가장 첫번째 결과만 저장
                recognized_text = text
            if text == practice_syllabus and confidence > 0.7:
                passed_ocr = True
                break
        
        recognized_texts[cell_id] = recognized_text if recognized_text is not None else ""  # 저장
        """당장은 ocr 통과했다고 가정하고 진행"""
        """실제로는 위의 코드를 사용하여 OCR을 통과했는지 확인해야 합니다."""
        passed_ocr = True

        # # OCR 실패 처리
        # if not passed_ocr:
        #     results.append({"score": 0, "stage": "OCR 실패"})
        #     print(f"Cell {cell_id} OCR 실패: {recognized_text} (기대값: {practice_syllabus})")
        #     fail_stage_counter["OCR 실패"] = fail_stage_counter.get("OCR 실패", 0) + 1
        #     continue


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

    # 3) Result 저장
    create_result(
        db, 
        mission_record.mission_id,
        avg_score,
    )
    
    # 4) 기준점수 넘으면 MissionRecord 업데이트
    PASSING_SCORE = 0.0
    if avg_score >= PASSING_SCORE:
        clear_mission_record(db, mission_record.mission_id)  # 내부에서 isCleared=True, clear_time=now() 처리


    # 5) Response 반환
    return ResultResponse(score=avg_score,
        summary=f"평균 점수: {avg_score}, 가장 많이 실패한 단계: {most_failed}",
        recognized_texts=recognized_texts)
          # OCR로 인식된 글자들 추가
    






