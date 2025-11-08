import cv2
import numpy as np

from .bboxtest import get_bbox_center
from .bboxtest import dist_smallchar
from .bboxtest import get_bbox_smallchar

from .decompose import char_decompose
from .image_utils import prepare_images_for_check
from .Rules import CHAR_TYPE_RULES

from .feedback import ERROR_FEEDBACK_4TH_CHILD as FEEDBACK_CHILD
from .feedback import ERROR_FEEDBACK_4TH_ADULT as FEEDBACK_ADULT
from .feedback import ERROR_FEEDBACK_4TH_FOREIGN as FEEDBACK_FOREIGN

"""

# 글자의 구도 종류 고르는 함수. 가-0 갈-1 두-2 둡-3

def get_char_type(y):
    type = 0

    return type
"""

#4차 스테이지 : 디테일 평가 (구버전)
def get_char_acc_old(images, phoneme_img_list, stroke_points, practice_syllabus):
    #char_type = get_char_type(char_info)

    char_type = -1

    char_decom = char_decompose(practice_syllabus)

    if char_decom[0][2] == ' ':
        if CHAR_TYPE_RULES[char_decom[0][1]] == 0:
            char_type = 0
        elif CHAR_TYPE_RULES[char_decom[0][1]] == 2:
            char_type = 2
        else:
            char_type = 4
    else:
        if CHAR_TYPE_RULES[char_decom[0][1]] == 0:
            char_type = 1
        elif CHAR_TYPE_RULES[char_decom[0][1]] == 2:
            char_type = 3
        else:
            char_type = 5

    if char_type == 1 or char_type == 3 or char_type == 5:

        char = np.array(images[0])
        Cell_1 = np.array(images[1])
        Cell_2 = np.array(images[2])
        Cell_3 = np.array(images[3])

        #img = cv2.imread(img_full)
        #img_1 = cv2.imread(img_cell_1)
        #img_2 = cv2.imread(img_cell_2)
        #img_3 = cv2.imread(img_cell_3)

        char_coord = get_bbox_smallchar(char)
        Cell_1_coord = get_bbox_smallchar(Cell_1)
        Cell_2_coord = get_bbox_smallchar(Cell_2)
        Cell_3_coord = get_bbox_smallchar(Cell_3)


        char_size = (char_coord[1][0] - char_coord[0][0]) * (char_coord[2][1] - char_coord[0][1])

        errormsg = ""

        if char_size == 0:
            errormsg = errormsg+ ("글씨가 너무 작아 알아볼 수 없어요...\n")
            return False, errormsg, None

        Cell_1_size = (Cell_1_coord[1][0] - Cell_1_coord[0][0]) * (Cell_1_coord[2][1] - Cell_1_coord[0][1])
        Cell_2_size = (Cell_2_coord[1][0] - Cell_2_coord[0][0]) * (Cell_2_coord[2][1] - Cell_2_coord[0][1])
        Cell_3_size = (Cell_3_coord[1][0] - Cell_3_coord[0][0]) * (Cell_3_coord[2][1] - Cell_3_coord[0][1])

        if char_type == 1:
            #   사이즈에 대한 오류를 에러 코드로 표시한 후, return하고 한 번에 출력하는 것은 어떤가?
            Cell_ratio_1_ans = 0.19369323922834714
            Cell_ratio_2_ans = 0.2088962039269306
            Cell_ratio_3_ans = 0.23924792306962553

            if Cell_1_size / char_size > Cell_ratio_1_ans * 1.4:
                errormsg = errormsg + ("초성의 크기가 너무 커요...\n")
            elif Cell_1_size / char_size < Cell_ratio_1_ans * 0.6:
                errormsg = errormsg + ("초성의 크기가 너무 작아요...\n")

            if Cell_2_size / char_size > Cell_ratio_2_ans * 1.4:
                errormsg = errormsg + ("중성의 크기가 너무 커요...\n")
            elif Cell_2_size / char_size < Cell_ratio_2_ans * 0.6:
                errormsg = errormsg + ("중성의 크기가 너무 작아요...\n")

            if Cell_3_size / char_size > Cell_ratio_3_ans * 1.4:
                errormsg = errormsg + ("종성의 크기가 너무 커요...\n")
            elif Cell_3_size / char_size < Cell_ratio_3_ans * 0.6:
                errormsg = errormsg + ("종성의 크기가 너무 작아요...\n")

        elif char_type == 3:

            Cell_ratio_1_ans = 0.2160306845003934
            Cell_ratio_2_ans = 0.22580645161290322
            Cell_ratio_3_ans = 0.23797736488531138

            if Cell_1_size / char_size > Cell_ratio_1_ans * 1.4:
                errormsg = errormsg + ("초성의 크기가 너무 커요...\n")
            elif Cell_1_size / char_size < Cell_ratio_1_ans * 0.6:
                errormsg = errormsg + ("초성의 크기가 너무 작아요...\n")

            if Cell_2_size / char_size > Cell_ratio_2_ans * 1.4:
                errormsg = errormsg + ("중성의 크기가 너무 커요...\n")
            elif Cell_2_size / char_size < Cell_ratio_2_ans * 0.6:
                errormsg = errormsg + ("중성의 크기가 너무 작아요...\n")

            if Cell_3_size / char_size > Cell_ratio_3_ans * 1.4:
                errormsg = errormsg + ("종성의 크기가 너무 커요...\n")
            elif Cell_3_size / char_size < Cell_ratio_3_ans * 0.6:
                errormsg = errormsg + ("종성의 크기가 너무 작아요...\n")

        elif char_type == 5:

            Cell_ratio_1_ans = 0.2327110698845472
            Cell_ratio_2_ans = 0.7165095824153981
            Cell_ratio_3_ans = 0.19951632406287786

            if Cell_1_size / char_size > Cell_ratio_1_ans * 1.4:
                errormsg = errormsg + ("초성의 크기가 너무 커요...\n")
            elif Cell_1_size / char_size < Cell_ratio_1_ans * 0.6:
                errormsg = errormsg + ("초성의 크기가 너무 작아요...\n")

            if Cell_2_size / char_size > Cell_ratio_2_ans * 1.4:
                errormsg = errormsg + ("중성의 크기가 너무 커요...\n")
            elif Cell_2_size / char_size < Cell_ratio_2_ans * 0.6:
                errormsg = errormsg + ("중성의 크기가 너무 작아요...\n")

            if Cell_3_size / char_size > Cell_ratio_3_ans * 1.4:
                errormsg = errormsg + ("종성의 크기가 너무 커요...\n")
            elif Cell_3_size / char_size < Cell_ratio_3_ans * 0.6:
                errormsg = errormsg + ("종성의 크기가 너무 작아요...\n")


    else:
        char = np.array(images[0])
        Cell_1 = np.array(images[1])
        Cell_2 = np.array(images[2])

        char_coord = get_bbox_smallchar(char)
        Cell_1_coord = get_bbox_smallchar(Cell_1)
        Cell_2_coord = get_bbox_smallchar(Cell_2)


        char_size = (char_coord[1][0] - char_coord[0][0]) * (char_coord[2][1] - char_coord[0][1])
        errormsg = ""

        if char_size == 0:
            errormsg = errormsg+ ("글씨가 너무 작아 알아볼 수 없어요...\n")
            return False, errormsg, None
        Cell_1_size = (Cell_1_coord[1][0] - Cell_1_coord[0][0]) * (Cell_1_coord[2][1] - Cell_1_coord[0][1])
        Cell_2_size = (Cell_2_coord[1][0] - Cell_2_coord[0][0]) * (Cell_2_coord[2][1] - Cell_2_coord[0][1])


        if char_type == 0:

            Cell_ratio_1_ans = 0.29048645096380044
            Cell_ratio_2_ans = 0.3886838868388684

            if Cell_1_size / char_size > Cell_ratio_1_ans * 1.4:
                errormsg = errormsg + ("초성의 크기가 너무 커요...\n")
            elif Cell_1_size / char_size < Cell_ratio_1_ans * 0.6:
                errormsg = errormsg + ("초성의 크기가 너무 작아요...\n")

            if Cell_2_size / char_size > Cell_ratio_2_ans * 1.4:
                errormsg = errormsg + ("중성의 크기가 너무 커요...\n")
            elif Cell_2_size / char_size < Cell_ratio_2_ans * 0.6:
                errormsg = errormsg + ("중성의 크기가 너무 작아요...\n")

        elif char_type == 2:

            Cell_ratio_1_ans = 0.3032908672759184
            Cell_ratio_2_ans = 0.45161290322580644

            if Cell_1_size / char_size > Cell_ratio_1_ans * 1.4:
                errormsg = errormsg + ("초성의 크기가 너무 커요...\n")
            elif Cell_1_size / char_size < Cell_ratio_1_ans * 0.6:
                errormsg = errormsg + ("초성의 크기가 너무 작아요...\n")

            if Cell_2_size / char_size > Cell_ratio_2_ans * 1.4:
                errormsg = errormsg + ("중성의 크기가 너무 커요...\n")
            elif Cell_2_size / char_size < Cell_ratio_2_ans * 0.6:
                errormsg = errormsg + ("중성의 크기가 너무 작아요...\n")

        elif char_type == 4:

            Cell_ratio_1_ans = 0.25411096466453276
            Cell_ratio_2_ans = 1.0

            if Cell_1_size / char_size > Cell_ratio_1_ans * 1.4:
                errormsg = errormsg + ("초성의 크기가 너무 커요...\n")
            elif Cell_1_size / char_size < Cell_ratio_1_ans * 0.6:
                errormsg = errormsg + ("초성의 크기가 너무 작아요...\n")

            if Cell_2_size / char_size > Cell_ratio_2_ans * 1.4:
                errormsg = errormsg + ("중성의 크기가 너무 커요...\n")
            elif Cell_2_size / char_size < Cell_ratio_2_ans * 0.6:
                errormsg = errormsg + ("중성의 크기가 너무 작아요...\n")


    if errormsg == "":
        return True, None, None
    else:
        return False, errormsg, None
    
def get_char_acc(images, phoneme_img_list, stroke_points, practice_syllabus, user_type):
    return get_char_acc_integrated(images, phoneme_img_list, stroke_points, practice_syllabus, user_type) #최종 통합 버전 사용
                

#4차 스테이지 : 음절 디테일 평가 (신버전) || 현재 사용중
def get_char_acc_final(img_tot, images, stroke_counts, practice_syllabus, user_type):

    """
    글자의 디테일 요소 (크기 밸런스, 자모 거리, 기울기 등) 평가 (4차 필터)

    Parameters:
        img_tot (bytes): 병합된 글자 이미지 (PNG 포맷의 바이트)
        images : 자모 이미지
        stroke_counts (list): 획 개수 리스트 (자모 분리용 기준)
        practice_syllabus (str): 기준 글자
        user_type (str): 유저의 나이 정보
    
    Returns:
        tuple(bool, str or None, str or None):
            - bool: 필터 통과 여부
            - str: 실패 이유 (통과 시 None)
            - str: 디버그용 내부 상태
    """

    # --- 설정 ---
    TOLERANCE_UPPER = 1.4
    TOLERANCE_LOWER = 0.6
    RATIO_RULES = {
        0: (0.29048, 0.38868),                      # 받침X, 세로모음 (가)
        1: (0.19369, 0.20889, 0.23924),             # 받침O, 세로모음 (각)
        2: (0.30329, 0.45161),                      # 받침X, 가로모음 (고)
        3: (0.21603, 0.22580, 0.23797),             # 받침O, 가로모음 (곡)
        4: (0.25411, 1.0),                          # 받침X, 복합모음 (과)
        5: (0.23271, 0.71650, 0.19951)              # 받침O, 복합모음 (곽)
    }

    # --- 내부 헬퍼 함수: 면적 계산 ---
    def _calculate_area(pil_image):
        bw_image = pil_image.convert("L")
        img_array = np.array(bw_image)
        is_char_mask = img_array < 255
        if not np.any(is_char_mask): return 0
        rows, cols = np.where(np.any(is_char_mask, axis=1))[0], np.where(np.any(is_char_mask, axis=0))[0]
        return (cols[-1] - cols[0] + 1) * (rows[-1] - rows[0] + 1)

    # --- 1. 이미지 준비 ---
    image_list = prepare_images_for_check(img_tot, images, stroke_counts)

    # --- 2. 한글 구조 분석 ---
    try:
        char_decom = char_decompose(practice_syllabus)
        has_jongseong = char_decom[0][2] != ' '
        vowel_type = CHAR_TYPE_RULES[char_decom[0][1]]

        if not has_jongseong:
            if vowel_type == 0: char_type = 0       # 받침X, 세로모음 (가)
            elif vowel_type == 2: char_type = 2     # 받침X, 가로모음 (고)
            else: char_type = 4                     # 받침X, 복합모음 (과)
        else:
            if vowel_type == 0: char_type = 1       # 받침O, 세로모음 (각)
            elif vowel_type == 2: char_type = 3     # 받침O, 가로모음 (곡)
            else: char_type = 5                     # 받침O, 복합모음 (곽)
    except Exception:
        return False, f"'{practice_syllabus}' 글자 구조를 분석할 수 없어요.", None

    # --- 3. 면적 계산 ---
    char_img, *jamo_images = image_list
    char_size = _calculate_area(char_img)

    #크기 계산이 안되는 경우
    if char_size == 0:
        return False, "글씨가 너무 작아 알아볼 수 없어요...", None
    

    cell_sizes = [_calculate_area(img) for img in jamo_images]
    
    # --- 4. 크기 비율 검사 ---
    ans_ratios = RATIO_RULES.get(char_type)
    if ans_ratios is None:
        return False, f"'{practice_syllabus}' 글자 (타입 {char_type})에 대한 규칙을 찾을 수 없어요.", None

    component_names, errors = ["초성", "중성", "종성"], []
    for i, size in enumerate(cell_sizes):
        if i >= len(ans_ratios): continue
        ratio, ans_ratio, name = size / char_size, ans_ratios[i], component_names[i]
        if ratio > ans_ratio * TOLERANCE_UPPER: errors.append(f"{name}의 크기가 너무 커요...")
        elif ratio < ans_ratio * TOLERANCE_LOWER: errors.append(f"{name}의 크기가 너무 작아요...")
            
    # --- 5. 최종 결과 반환 ---
    
    # --- 디버그 정보 생성 (성공/실패와 상관없이 항상 생성) ---
    debug_lines = []
    header = (
        f"입력 글자: '{practice_syllabus}' (타입: {char_type})\n"
        f"글자의 전체크기: {char_size}px\n"
    )
    debug_lines.append(header)

    for i, size in enumerate(cell_sizes):
        # cell_sizes와 ans_ratios 길이가 다를 수 있으므로 안전장치 추가
        if i >= len(ans_ratios): continue
            
        ratio = size / char_size
        ans_ratio = ans_ratios[i]
        name = component_names[i]
        
        line = f"[{name}] 크기: {size}px | 계산 비율: {ratio:.3f} | 정답 비율: {ans_ratio:.3f}"
        debug_lines.append(line)
    
    final_debug_string = "\n".join(debug_lines)

    # --- 오류 여부에 따라 결과와 함께 디버그 정보 반환 ---
    if not errors:
        return True, None, final_debug_string
    else:
        return False, "\n".join(errors), final_debug_string
    

    # 최종 통합 버전:
def get_char_acc_integrated(img_tot, images, stroke_counts, practice_syllabus, user_type):
    """
    글자의 디테일 요소 (자모별 크기, 가로세로 비율)를 종합적으로 평가 (최종 필터)

    Parameters:
        img_tot (bytes): 병합된 글자 이미지 (PNG 포맷의 바이트)
        images (list): 분리된 자모 이미지 리스트
        stroke_counts (list): 획 개수 리스트 (자모 분리용 기준)
        practice_syllabus (str): 평가의 기준이 되는 글자 (예: '각')
    
    Returns:
        tuple(bool, str or None, str or None):
            - bool: 필터 통과 여부
            - str: 실패 이유 (통과 시 None)
            - str: 디버그용 내부 상태 정보
    """

    # --- 설정: 허용 오차 범위와 규칙을 적용 ---
    TOLERANCE_UPPER = 1.5
    TOLERANCE_LOWER = 0.5

    # 유저 타입 설정
    FEEDBACK_STR = None
    
    if user_type == "CHILD":
        FEEDBACK_STR = FEEDBACK_CHILD
    elif user_type == "ADULT":
        FEEDBACK_STR = FEEDBACK_ADULT
    elif user_type == "FOREIGN":
        FEEDBACK_STR = FEEDBACK_FOREIGN
    else:
        FEEDBACK_STR = FEEDBACK_FOREIGN
        
    # 규칙: (자모 크기 비율, 자모 가로세로 비율)을 튜플로 묶어서 관리
    RATIO_RULES = {
        # 받침 O (초성, 중성, 종성)
        "종성있음": {
            0: ((0.2813, 1.0), (0.2124, 0.5826), (0.2214, 1.5068)),
            1: ((0.3401, 1.0), (0.2761, 0.6260), (0.2702, 1.5205)),
            2: ((0.2314, 1.9206), (0.2967, 3.3518), (0.3183, 1.2391)),
            3: ((0.2460, 1.8059), (0.6538, 1.5210), (0.2387, 1.6521)),
            4: ((0.2636, 1.7042), (0.0888, 11.3125), (0.2484, 1.6056)),
            5: ((0.3516, 1.0), (0.1110, 0.2434), (0.2768, 1.5068)),
            6: ((0.2876, 0.9009), (0.2453, 0.5726), (0.2466, 1.5633)),
            7: ((0.2876, 0.9009), (0.3315, 0.7478), (0.2466, 1.5633)),
            8: ((0.1910, 1.5), (0.5969, 1.3162), (0.2500, 1.6323)),
            9: ((0.1989, 1.4307), (0.6428, 1.2301), (0.2667, 1.5205)),
            10: ((0.1700, 1.0845), (0.6326, 1.3225), (0.6422, 0.5967)),
            11: ((0.1394, 1.4727), (0.6071, 1.3697), (0.2327, 1.6567)),
            12: ((0.1744, 1.5423), (0.6275, 1.2764), (0.2344, 1.7076)),
            13: ((0.1581, 1.5), (0.6071, 1.5630), (0.2021, 1.6417)),
            14: ((0.1897, 1.5), (0.6632, 1.1923), (0.2447, 1.6567)),
        },
        # 받침 X (초성, 중성)
        "종성없음": {
            0: ((0.3236, 0.9035), (0.3636, 0.3505)),
            1: ((0.3930, 0.9035), (0.4805, 0.3814)),
            2: ((0.4997, 1.2828), (0.5611, 2.3205)),
            3: ((0.3153, 1.5875), (0.5730, 1.7745)),
            4: ((0.5494, 1.1467), (0.1167, 11.3125)),
            5: ((0.4035, 0.9035), (0.1866, 0.1443)),
            6: ((0.3063, 0.7909), (0.4347, 0.3608)),
            7: ((0.3063, 0.7909), (0.5652, 0.4690)),
            8: ((0.2467, 1.2763), (1.0, 0.7938)),
            9: ((0.2387, 1.3108), (1.0, 0.7989)),
            10: ((0.1623, 1.3016), (1.0, 0.8453)),
            11: ((0.1806, 1.2352), (1.0, 0.8402)),
            12: ((0.2229, 1.3857), (1.0, 0.8092)),
            13: ((0.2021, 1.2631), (1.0, 0.9587)),
            14: ((0.2290, 1.3661), (1.0, 0.7989)),
        }
    }
    
    # --- 내부 헬퍼 함수: 면적과 가로세로 비율 계산 ---
    def _calculate_metrics(pil_image):
        bw_image = pil_image.convert("L")
        img_array = np.array(bw_image)
        is_char_mask = img_array < 255
        
        if not np.any(is_char_mask): return 0, 0

        rows = np.where(np.any(is_char_mask, axis=1))[0]
        cols = np.where(np.any(is_char_mask, axis=0))[0]
        
        height = rows[-1] - rows[0] + 1
        width = cols[-1] - cols[0] + 1

        area = width * height
        aspect_ratio = width / height if height > 0 else 0
        return area, aspect_ratio

    # --- 1. 이미지 준비 ---
    image_list = prepare_images_for_check(img_tot, images, stroke_counts)

    # --- 2. 한글 구조 분석 ---
    try:
        char_decom = char_decompose(practice_syllabus)
        has_jongseong = char_decom[0][2] != ' '

        char_type = CHAR_TYPE_RULES[char_decom[0][1]] 
    except Exception:
        return False, f"'{practice_syllabus}' 글자 구조를 분석할 수 없어요.", None

    # --- 3. 면적 및 비율 계산 ---
    char_img, *jamo_images = image_list
    char_size, _ = _calculate_metrics(char_img)

    if char_size == 0:
        return False, "글씨가 너무 작아 알아볼 수 없어요...", None
    
    cell_metrics = [_calculate_metrics(img) for img in jamo_images]
    
    # --- 4. 크기 및 가로세로 비율 검사 ---
    key = "종성있음" if has_jongseong else "종성없음"
    ans_ratios_set = RATIO_RULES.get(key, {}).get(char_type)

    if ans_ratios_set is None:
        return False, f"'{practice_syllabus}' 글자 (타입 {char_type})에 대한 규칙을 찾을 수 없어요.", None

    component_names, errors = [FEEDBACK_STR['FIRST_CELL'], FEEDBACK_STR['SECOND_CELL'], FEEDBACK_STR['THIRD_CELL']], []
    for i, metrics in enumerate(cell_metrics):
        if i >= len(ans_ratios_set): continue
        
        size, aspect_ratio = metrics
        ans_size_ratio, ans_aspect_ratio = ans_ratios_set[i]
        name = component_names[i]
        
        current_size_ratio = size / char_size if char_size > 0 else 0

        # 크기 검사 (상위 검사)
        if current_size_ratio > ans_size_ratio * TOLERANCE_UPPER:
            errors.append(f"{name}" + FEEDBACK_STR['TOO_BIG'])
            # 가로세로 비율 검사 (하위 검사)
            if aspect_ratio > ans_aspect_ratio * TOLERANCE_UPPER: errors.append(FEEDBACK_STR['TOO_BIG_HORIZONTAL'])
            elif aspect_ratio < ans_aspect_ratio * TOLERANCE_LOWER: errors.append(FEEDBACK_STR['TOO_BIG_VERTICAL'])
            else: errors.append(FEEDBACK_STR['TOO_BIG_NORMAL'])
        
        elif current_size_ratio < ans_size_ratio * TOLERANCE_LOWER:
            errors.append(f"{name}" + FEEDBACK_STR['TOO_SMALL'])
            # 가로세로 비율 검사 (하위 검사) 
            if aspect_ratio > ans_aspect_ratio * TOLERANCE_UPPER: errors.append(FEEDBACK_STR['TOO_SMALL_VERTICAL'])
            elif aspect_ratio < ans_aspect_ratio * TOLERANCE_LOWER: errors.append(FEEDBACK_STR['TOO_SMALL_HORIZONTAL'])
            else: errors.append(FEEDBACK_STR['TOO_SMALL_NORMAL'])

    # --- 5. 최종 결과 반환 ---
    # 디버그 정보 생성
    debug_lines = [
        f"입력 글자: '{practice_syllabus}' (타입: {char_type}, 종성유무: {has_jongseong})",
        f"전체 글자 크기: {char_size}px"
    ]
    for i, metrics in enumerate(cell_metrics):
        if i >= len(ans_ratios_set): continue
        size, aspect_ratio = metrics
        ans_size_ratio, ans_aspect_ratio = ans_ratios_set[i]
        name = component_names[i]
        
        line = (f"[{name}] 크기: {size}px | 면적비율: {size/char_size:.3f} (정답: {ans_size_ratio:.3f}) | "
                f"가로세로비: [{aspect_ratio:.3f} : 1] (정답: [{ans_aspect_ratio:.3f} : 1]) ")
        debug_lines.append(line)
    
    final_debug_string = "\n".join(debug_lines)

    if not errors:
        return True, None, final_debug_string
    else:
        return False, "\n".join(errors), final_debug_string
