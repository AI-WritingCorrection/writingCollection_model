import numpy as np
import io
from PIL import Image


from .bboxtest import get_bbox_smallchar
from .feedback import ERROR_FEEDBACK_2ND_CHILD as FEEDBACK_CHILD
from .feedback import ERROR_FEEDBACK_2ND_ADULT as FEEDBACK_ADULT
from .feedback import ERROR_FEEDBACK_2ND_FOREIGN as FEEDBACK_FOREIGN

# 2차 스테이지: 크기 및 비율 검사

def check_char_size(img_tot, user_type, version = "new"):
    if version == "old":
        return check_char_size_old(img_tot)
    else:
        return check_char_size_new(img_tot, user_type)


#old version : 방식 - 경계선 스캔을 통해 글자 크기 비율 판단 [경계선 스캔 방식]
def check_char_size_old(images):
    errormsg = ""
    
    img = np.array(images[0])
    img_x = len(img[0])
    img_y = len(img)

    cell_coord = get_bbox_smallchar(img)
    cell_x = cell_coord[1][0] - cell_coord[0][0]
    cell_y = cell_coord[2][1] - cell_coord[0][1]

    ratio_x = cell_x / img_x
    ratio_y = cell_y / img_y

    if ratio_x > 0.85:
        errormsg = errormsg + "글씨가 가로로 너무 커요...\n"
    elif ratio_x < 0.5:
        errormsg = errormsg + "글씨가 가로로 너무 작아요...\n"

    if ratio_y > 0.85:
        errormsg = errormsg + "글씨가 세로로 너무 커요...\n"
    elif ratio_y < 0.5:
        errormsg = errormsg + "글씨가 세로로 너무 작아요...\n"

    if errormsg == "":
        return True, None
    else:
        return False, errormsg

#new version : 방식 - numpy로 글자 영역 탐색 후 크기 비율 판단 [그림자 찾기 방식]
#2차 스테이지 보완
def check_char_size_new(img_tot, user_type):
    """
    PNG 바이트 이미지를 받아 내부 글씨의 크기 비율을 검사한다.
    NumPy를 사용해 효율적으로 글씨 영역(bounding box)을 찾는다.
    
    Args:
        img_tot (bytes): PNG 포맷의 이미지 바이트 데이터
        
    Returns:
        (bool, str or None, str or None): (성공 여부, 오류 메시지, 디버그 메시지)
    """
    # --- 설정: 글씨 크기 비율 제한 (여기서 값을 쉽게 수정) ---
    MAX_WIDTH_RATIO = 0.85
    MIN_WIDTH_RATIO = 0.5
    MAX_HEIGHT_RATIO = 0.85
    MIN_HEIGHT_RATIO = 0.5
    
    # --- 설정: 유저 타입에 따른 피드백 준비 ---
    FEEDBACK_STR = None
    
    if user_type == 'CHILD':
        FEEDBACK_STR = FEEDBACK_CHILD
    elif user_type == 'ADULT':
        FEEDBACK_STR = FEEDBACK_ADULT
    elif user_type == 'FOREIGN':
        FEEDBACK_STR = FEEDBACK_FOREIGN
    else:
        FEEDBACK_STR = FEEDBACK_ADULT
        
    # --- 1. 이미지 데이터 준비 ---
    try:
        # 바이트 데이터를 Pillow 이미지로 열고, 채널을 RGBA로 통일
        pil_image = Image.open(io.BytesIO(img_tot)).convert("RGBA")
        img = np.array(pil_image)
    except Exception:
        return False, "이미지 파일을 여는 데 실패했어요.", None

   # --- 2. NumPy로 글씨 영역 초고속 탐색 (색상 기준) ---
    # 이미지를 흑백(Luminance)으로 변환. 흰색(255)과 나머지(255 미만)로 구분하기 위함.
    bw_image = pil_image.convert("L")
    img = np.array(bw_image)

    # 흰색이 아닌 픽셀(글씨)이 있는지 확인. 
    # bw_img < 255 는 흰색이 아닌 모든 픽셀을 True로 표시.
    is_char_mask = img < 255
    if not np.any(is_char_mask):
        return False, "이미지에 글씨가 없거나 전체가 흰색이에요.", None
        
    # 글씨가 있는 행(row)과 열(column)의 인덱스를 찾는다 (그림자 찾기 방식은 동일)
    rows = np.where(np.any(is_char_mask, axis=1))[0]
    cols = np.where(np.any(is_char_mask, axis=0))[0]
    
    top, bottom = rows[0], rows[-1]
    left, right = cols[0], cols[-1]
    
    # --- 3. 크기 및 비율 계산 ---
    img_h, img_w = img.shape[:2]      # 전체 이미지 높이, 너비
    char_h = bottom - top + 1         # 실제 글씨 높이
    char_w = right - left + 1         # 실제 글씨 너비
    
    ratio_x = char_w / img_w
    ratio_y = char_h / img_h
    

    # --- 디버그 메세지 : 내부 상태 문자열로 반환 ---
    debug_msg = (f"이미지 크기: {img_w}x{img_h}, 글씨 크기: {char_w}x{char_h}, "
                     f"너비 비율: {ratio_x:.2f}, 높이 비율: {ratio_y:.2f}")
    
    # --- 4. 오류 메시지 생성 (통합 메시지 로직 적용) ---
    is_too_wide = ratio_x > MAX_WIDTH_RATIO
    is_too_narrow = ratio_x < MIN_WIDTH_RATIO
    is_too_tall = ratio_y > MAX_HEIGHT_RATIO
    is_too_short = ratio_y < MIN_HEIGHT_RATIO


    errors = []
    # CASE 1: 둘 다 너무 클 때
    if is_too_wide and is_too_tall:
        msg = FEEDBACK_STR['TOO_BIG'] + '\n' + FEEDBACK_STR['TOO_BIG_NORMAL']
        errors.append(msg)
    # CASE 2: 둘 다 너무 작을 때
    elif is_too_narrow and is_too_short:
        msg = FEEDBACK_STR['TOO_SMALL'] + '\n' + FEEDBACK_STR['TOO_SMALL_NORMAL']
        errors.append(msg)
    # CASE 3: 그 외 개별적인 오류들
    else:
        if is_too_wide:
            msg = FEEDBACK_STR['TOO_BIG_HORIZONTAL']
            errors.append(msg)
        elif is_too_narrow:
            msg = FEEDBACK_STR['TOO_SMALL_HORIZONTAL']
            errors.append(msg)

        if is_too_tall:
            msg = FEEDBACK_STR['TOO_BIG_VERTICAL']
            errors.append(msg)
        elif is_too_short:
            msg = FEEDBACK_STR['TOO_BIG_VERTICAL']
            errors.append(msg)

        
    # --- 5. 최종 결과 반환 ---
    if not errors:
        return True, None, debug_msg
    else:
        return False, "\n".join(errors), debug_msg

