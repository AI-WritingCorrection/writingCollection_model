from fastapi import APIRouter, Depends
from database import get_db
from dto.resultDTO import ResultCreate, ResultResponse
from service.missionRecordService import clear_mission_record, create_mission_record
from service.resultService import create_result
from aiModel.utils.image_utils import merge_images
from aiModel.utils.image_utils import decode_base64_image_list
from aiModel.utils.font_score_utils import evaluate_character
from aiModel.utils.stroke_utils import count_jamo_matches, has_jongseung, extract_letters #1차 스테이지 보완

from sqlalchemy.orm import Session

from service.userService import get_user_by_id

router=APIRouter()

reader = None  # will be initialized lazily

@router.post("/evaluate", response_model=ResultResponse)
async def evaluate_handwriting(payload: ResultCreate,  db: Session = Depends(get_db)):
    global reader
    if reader is None:
        from aiModel import easyocr_mk2 as easyocr # 수정된 easyocr 모듈 임포트
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
        ocr_results = reader.readtext(img_bytes, detail = 0, decoder = 'greedy')  # detail=0 으로 설정하여 (text, confidence) 튜플 대신 텍스트만 반환

        # 4. OCR 결과 확인
        passed_ocr = False

        # 4_a. 정확히 맞으면 통과
        recognized_text = ocr_results[0] if ocr_results else None  # 기본값 설정
        if recognized_text == practice_syllabus : # 정확히 맞는 경우
            recognized_texts[cell_id] = "완벽 => " + recognized_text  # 저장
            passed_ocr = True
            

        # 4_b. 틀렸지만 후보군내에서 자모음이 맞는 경우가 있을 시 통과
        else : 
            # 3. OCR_TOP K
            ocr_results = reader.readtext(img_bytes, detail = 0, decoder = 'greedy_best2')  # detail=0 으로 설정하여 (text, confidence) 튜플 대신 텍스트만 반환
            recognized_text = ocr_results[0] if ocr_results else None  # 기본값 설정

            eval_count = 2 if has_jongseung(practice_syllabus) else 2 # 종성이 있으면 초중종[3], 없으면 초중[2]  인데 일단 2로 통일
            if eval_count <= count_jamo_matches(recognized_text, practice_syllabus) :
                recognized_texts[cell_id] = "괜찮음(후보군) => " + extract_letters(recognized_text)
                passed_ocr = True

        # 이게 틀린거 요약 + 교정 내용 조금 추가 할 필요 있음 지금은 일단 꺼둠 return 작업자가 수정해줘야함.
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
            "stage": score_result["stage"],
            "feedback" : score_result["reason"],
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
        summary=f"가장 많이 실패한 단계: {most_failed}",
        feedback=results["feedback"])
          # OCR로 인식된 글자들 추가
