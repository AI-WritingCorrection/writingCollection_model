from .image_utils import merge_images
from .image_utils import split_and_merge_images
from .char_accr import check_char_size
from .stroke_utils import check_stroke_directions
from .cell_accr import get_char_acc

def evaluate_character(passed_ocr, images, stroke_counts, stroke_points, practice_syllabus, user_type):
    """
    글자 하나에 대한 평가 함수: 2차 (크기), 3차 (획 순서), 4차 (디테일)를 순차적으로 통과시킴 | 1차는 ocr 통과로 간주

    Parameters:
        passed_ocr (bool): OCR 통과 여부
        images (list[PIL.Image.Image]): 디코딩된 획 이미지 리스트
        stroke_counts (list[int]): 획 수 정보
        stroke_points (list[dict]): 획의 시작점/끝점 좌표 정보
        practice_syllabus (str): 기준 글자
        user_type (str): 피드백 문장 타입 선정을 위한 유저 정보

    Returns:
        dict: 평가 결과
            - stage (str): 실패한 단계 또는 "완료"
            - reason (str): 실패 피드백
            - score (int): 누적 점수
    """

    #초기 값 설정

    #0 =통과 , 1=실패, ex0010 == 3번 스테이지에서만 실패
    error_stage = "0" if passed_ocr else "1" #  문제가 생긴 단계 저장 (0: OCR 통과, 1: OCR 불통과)
    
    
    # 4칸짜리 리스트로 초기화, 각 칸은 각 단계를 의미
    error_reason = [None, None, None, None]
    if not passed_ocr:
        error_reason[0] = "글자를 인식하지 못했어요." # 1단계(OCR) 실패 피드백
    
    score = 50 if passed_ocr else 0 # 1차(OCR)통과 시 50점, 불통과 시 0점

    # 획 -> 글자 이미지 병합
    img_tot = merge_images(images)

    # 음소 단위로 병합된 이미지 바이트 리스트
    phoneme_img_list = split_and_merge_images(images, stroke_counts)
    """
    phoneme_img_list[0] → 초성,
    phoneme_img_list[1] → 중성,
    phoneme_img_list[2] → 종성 (종성 없는 글자인 경우 없음)
    """


    # 2차 필터: 전체 형태 (크기 및 비율)
    passed, reason, stage2_debug_state = check_shape(img_tot, user_type)
    if not passed:
        error_stage += "1"
        error_reason[1] = reason
        # return {"stage": "2차 필터", "reason": reason, "score": score}
    else:
        error_stage += "0"
        score += 20

    
    # 3차 필터: 획 순서
    passed, reason, stage3_debug_state = check_stroke_order(stroke_points, practice_syllabus)
    if not passed:
        error_stage += "1"
        error_reason[2] = reason
        # return {"stage": "3차 필터", "reason": reason, "score": score}
    else:
        error_stage += "0"
        score += 15


    # 4차 필터: 디테일 평가
    passed, reason, stage4_debug_state = check_detail_features(img_tot, images, stroke_counts, practice_syllabus, user_type)
    if not passed:
        error_stage += "1"
        error_reason[3] = reason
        # return {"stage": "4차 필터", "reason": reason, "score": score}
    else:
        error_stage += "0"
        score += 15

    # 필요없음 확인후 제거
    # if score == 100:
    #     error_stage.append("완료")
    #     error_reason.append(None)
    #     # return {"stage": "완료", "reason": None, "score": score}

    return {"stage": error_stage, "reason": error_reason, "score": score,
             "stage2_debug_state": stage2_debug_state, "stage3_debug_state": stage3_debug_state, "stage4_debug_state": stage4_debug_state}


# 2차 필터: 전체 형태 (크기 및 비율)
def check_shape(img_tot, user_type, version = "new"):
    """
    병합된 글자 이미지의 크기/비율을 판단하는 함수 (2차 필터)

    Parameters:
        img_tot (bytes): 병합된 글자 이미지 (PNG 포맷의 바이트)

    Returns:
        tuple(bool, str or None):
            - bool: 필터 통과 여부
            - str: 실패 이유 (통과 시 None)
            - str: 디버그용 내부 상태
    """

    is_passed, reason, debug_msg = check_char_size(img_tot , user_type, version)

    return is_passed, reason, debug_msg



# 3차 필터: 획 순서
def check_stroke_order(stroke_points, practice_syllabus):
    """
    획의 방향과 순서가 올바른지 판단 (3차 필터)

    Parameters:
        stroke_points (list[dict]): 획별 시작/끝 좌표
        practice_syllabus (str): 기준 글자 (예: '가', '밈')

    Returns:
        tuple(bool, str or None):
            - bool: 필터 통과 여부
            - str: 실패 이유 (통과 시 None)
    """

    is_passed, reason, stage3_debug_state = check_stroke_directions(practice_syllabus, stroke_points)

    return is_passed, reason, stage3_debug_state


# 4차 필터: 디테일 평가
def check_detail_features(img_tot, images, stroke_counts, practice_syllabus, user_type):
    """
    글자의 디테일 요소 (크기 밸런스, 자모 거리, 기울기 등) 평가 (4차 필터)

    Parameters:
        images : 자모 이미지
        phoneme_img_list (list[bytes]): 초성/중성/종성 병합 이미지 바이트 리스트
        stroke_points (list[dict]): 획 좌표 정보 (자모 분리용 기준)
        practice_syllabus (str): 기준 글자
        user_type: 유저의 나이 정보

    Returns:
        tuple(bool, str or None):
            - bool: 필터 통과 여부
            - str: 실패 이유 (통과 시 None)
    """

    is_passed, reason, stage4_debug_state = get_char_acc(img_tot, images, stroke_counts, practice_syllabus, user_type)


    return is_passed, reason, stage4_debug_state


