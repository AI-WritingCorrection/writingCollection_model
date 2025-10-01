import cv2
import numpy as np

from .bboxtest import get_bbox_center
from .bboxtest import dist_smallchar
from .bboxtest import get_bbox_smallchar

from .decompose import char_decompose
from .image_utils import prepare_images_for_check
from .Rules import CHAR_TYPE_RULES

"""

# 글자의 구도 종류 고르는 함수. 가-0 갈-1 두-2 둡-3

def get_char_type(y):
    type = 0

    return type
"""

def get_char_acc(images, phoneme_img_list, stroke_points, practice_syllabus):
    return get_char_acc_final(images, phoneme_img_list, stroke_points, practice_syllabus)

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
                

#4차 스테이지 : 음절 디테일 평가 (신버전) || 현재 사용중
def get_char_acc_final(img_tot, images, stroke_counts, practice_syllabus):

    """
    글자의 디테일 요소 (크기 밸런스, 자모 거리, 기울기 등) 평가 (4차 필터)

    Parameters:
        img_tot (bytes): 병합된 글자 이미지 (PNG 포맷의 바이트)
        images : 자모 이미지
        stroke_counts (list): 획 개수 리스트 (자모 분리용 기준)
        practice_syllabus (str): 기준 글자
    
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