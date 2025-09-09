from .image_utils import merge_images
from .image_utils import split_and_merge_images
from .char_accr import check_char_size
from .stroke_utils import check_stroke_directions
from .cell_accr import get_char_acc

def evaluate_character(images, stroke_counts, stroke_points, practice_syllabus):
    """
    글자 하나에 대한 평가 함수: 2차 (크기), 3차 (획 순서), 4차 (디테일)를 순차적으로 통과시킴 | 1차는 ocr 통과로 간주

    Parameters:
        images (list[PIL.Image.Image]): 디코딩된 획 이미지 리스트
        stroke_counts (list[int]): 획 수 정보
        stroke_points (list[dict]): 획의 시작점/끝점 좌표 정보
        practice_syllabus (str): 기준 글자

    Returns:
        dict: 평가 결과
            - stage (str): 실패한 단계 또는 "완료"
            - reason (str): 실패 이유 (선택적)
            - score (int): 누적 점수
    """

    #초기 값 설정

    error_stage = []    #   문제가 생긴 단계 저장
    error_reason = ""   #   단계에서 감지한 문제 저장
    
    # 1차 필터 (OCR)는 서버 측에서 이미 통과한 것으로 간주하고 50점 부여
    score = 50 

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
    passed, reason = check_bbox_shape(images)
    if not passed:
        error_stage.append("2차 필터")
        error_reason = error_reason + reason
        # return {"stage": "2차 필터", "reason": reason, "score": score}
    else:
        score += 20

    
    # 3차 필터: 획 순서
    passed, reason = check_stroke_order(stroke_points, practice_syllabus)
    if not passed:
        error_stage.append("3차 필터")
        error_reason = error_reason + reason
        # return {"stage": "3차 필터", "reason": reason, "score": score}
    else:
        score += 15


    # 4차 필터: 디테일 평가
    passed, reason = check_detail_features(images, phoneme_img_list, stroke_points, practice_syllabus)
    if not passed:
        error_stage.append("4차 필터")
        error_reason = error_reason + reason
        # return {"stage": "4차 필터", "reason": reason, "score": score}
    else:
        score += 15

    if score == 100:
        error_stage.append("완료")
        error_reason.append(None)
        # return {"stage": "완료", "reason": None, "score": score}

    return {"stage": error_stage, "reason": error_reason, "score": score}


# 2차 필터: 전체 형태 (크기 및 비율)
def check_bbox_shape(images):
    """
    병합된 글자 이미지의 크기/비율을 판단하는 함수 (2차 필터)

    Parameters:
        img_tot (bytes): 병합된 글자 이미지 (PNG 포맷의 바이트)

    Returns:
        tuple(bool, str or None):
            - bool: 필터 통과 여부
            - str: 실패 이유 (통과 시 None)
    """
    is_passed, reason = check_char_size(images)
    return is_passed, reason



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

    is_passed, reason = check_stroke_directions(practice_syllabus, stroke_points)

    return is_passed, reason


# 4차 필터: 디테일 평가
def check_detail_features(images, phoneme_img_list, stroke_points, practice_syllabus):
    """
    글자의 디테일 요소 (크기 밸런스, 자모 거리, 기울기 등) 평가 (4차 필터)

    Parameters:
        images : 자모 이미지
        phoneme_img_list (list[bytes]): 초성/중성/종성 병합 이미지 바이트 리스트
        stroke_points (list[dict]): 획 좌표 정보 (자모 분리용 기준)
        practice_syllabus (str): 기준 글자

    Returns:
        tuple(bool, str or None):
            - bool: 필터 통과 여부
            - str: 실패 이유 (통과 시 None)
    """

    is_passed, reason = get_char_acc(images, phoneme_img_list, stroke_points, practice_syllabus)


    return is_passed, reason


