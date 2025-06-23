import cv2
import numpy as np

from .bboxtest import get_bbox_center
from .bboxtest import dist_smallchar
from .bboxtest import get_bbox_smallchar

from .decompose import char_decompose
from .Rules import CHAR_TYPE_RULES

"""

# 글자의 구도 종류 고르는 함수. 가-0 갈-1 두-2 둡-3

def get_char_type(y):
    type = 0

    return type
"""

def get_char_acc(images, phoneme_img_list, stroke_points, practice_syllabus):
    #char_type = get_char_type(char_info)

    char_type = -1
    
    char_decom = char_decompose(practice_syllabus)

    if char_decom[0][2] == '':
        if CHAR_TYPE_RULES[char_decom[0][1]] == 0:
            char_type = 0
        else:
            char_type = 2
    else:
        if CHAR_TYPE_RULES[char_decom[0][1]] == 0:
            char_type = 1
        else:
            char_type = 3
    
    if char_type == 1 or char_type == 3:
        
        img = np.array(images[0])
        img_1 = np.array(images[1])
        img_2 = np.array(images[2])
        img_3 = np.array(images[3])

        #img = cv2.imread(img_full)
        #img_1 = cv2.imread(img_cell_1)
        #img_2 = cv2.imread(img_cell_2)
        #img_3 = cv2.imread(img_cell_3)

        img_center = get_bbox_center(get_bbox_smallchar(img))
        img_1_center = get_bbox_center(get_bbox_smallchar(img_1))
        img_2_center = get_bbox_center(get_bbox_smallchar(img_2))
        img_3_center = get_bbox_center(get_bbox_smallchar(img_3))

        img_size = ((img_center[0] * 2) ** 2 + (img_center[1] * 2) ** 2) ** 0.5
        
        img_1_dist = dist_smallchar(img_center, img_1_center)
        img_2_dist = dist_smallchar(img_center, img_2_center)
        img_3_dist = dist_smallchar(img_center, img_3_center)

        dist_ratio_1 = dist_smallchar(img_center, img_1_center) / img_size
        dist_ratio_2 = dist_smallchar(img_center, img_2_center) / img_size
        dist_ratio_3 = dist_smallchar(img_center, img_3_center) / img_size

        errormsg = ""

        if char_type == 1:
            #   사이즈에 대한 오류를 에러 코드로 표시한 후, return하고 한 번에 출력하는 것은 어떤가?
            dist_ratio_1_ans = 0.207
            dist_ratio_2_ans = 0.24
            dist_ratio_3_ans = 0.192

            if dist_ratio_1 / dist_ratio_1_ans > 1.4:
                errormsg = errormsg + ("초성의 크기가 너무 커요...\n")
            elif dist_ratio_1 / dist_ratio_1_ans < 0.6:
                errormsg = errormsg + ("초성의 크기가 너무 작아요...\n")

            if dist_ratio_2 / dist_ratio_2_ans > 1.4:
                errormsg = errormsg + ("중성의 크기가 너무 커요...\n")
            elif dist_ratio_2 / dist_ratio_2_ans < 0.6:
                errormsg = errormsg + ("중성의 크기가 너무 작아요...\n")

            if dist_ratio_3 / dist_ratio_3_ans > 1.4:
                errormsg = errormsg + ("종성의 크기가 너무 커요...\n")
            elif dist_ratio_3 / dist_ratio_3_ans < 0.6:
                errormsg = errormsg + ("종성의 크기가 너무 작아요...\n")

        elif char_type == 3:
            
            dist_ratio_1_ans = 0.2
            dist_ratio_2_ans = 0.0017
            dist_ratio_3_ans = 0.19

            if dist_ratio_1 / dist_ratio_1_ans > 1.4:
                errormsg = errormsg + ("초성의 크기가 너무 커요...\n")
            elif dist_ratio_1 / dist_ratio_1_ans < 0.6:
                errormsg = errormsg + "초성의 크기가 너무 작아요...\n"

            if dist_ratio_2 / dist_ratio_2_ans > 1.4:
                errormsg = errormsg + ("중성의 크기가 너무 커요...\n")
            elif dist_ratio_2 / dist_ratio_2_ans < 0.6:
                errormsg = errormsg + ("중성의 크기가 너무 작아요...\n")

            if dist_ratio_3 / dist_ratio_3_ans > 1.4:
                errormsg = errormsg + ("종성의 크기가 너무 커요...\n")
            elif dist_ratio_3 / dist_ratio_3_ans < 0.6:
                errormsg = errormsg + ("종성의 크기가 너무 작아요...\n")
            
        
    else:
        img = np.array(images[0])
        img_1 = np.array(images[1])
        img_2 = np.array(images[2])

        img_center = get_bbox_center(get_bbox_smallchar(img))
        img_1_center = get_bbox_center(get_bbox_smallchar(img_1))
        img_2_center = get_bbox_center(get_bbox_smallchar(img_2))

        img_center = get_bbox_center(bt.get_bbox_smallchar(img))
        img_1_center = get_bbox_center(bt.get_bbox_smallchar(img_1))
        img_2_center = get_bbox_center(bt.get_bbox_smallchar(img_2))

        img_size = ((img_center[0] * 2) ** 2 + (img_center[1] * 2) ** 2) ** 0.5
        
        img_1_dist = dist_smallchar(img_center, img_1_center)
        img_2_dist = dist_smallchar(img_center, img_2_center)

        dist_ratio_1 = dist_smallchar(img_center, img_1_center) / img_size
        dist_ratio_2 = dist_smallchar(img_center, img_2_center) / img_size
        
        if char_type == 0:

            dist_ratio_1_ans = 0.163
            dist_ratio_2_ans = 0.192

            if dist_ratio_1 / dist_ratio_1_ans > 1.4:
                errormsg = errormsg + ("초성의 크기가 너무 커요...\n")
            elif dist_ratio_1 / dist_ratio_1_ans < 0.6:
                errormsg = errormsg + ("초성의 크기가 너무 작아요...\n")

            if dist_ratio_2 / dist_ratio_2_ans > 1.4:
                errormsg = errormsg + ("중성의 크기가 너무 커요...\n")
            elif dist_ratio_2 / dist_ratio_2_ans < 0.6:
                errormsg = errormsg + ("중성의 크기가 너무 작아요...\n")

        elif char_type == 2:
            
            dist_ratio_1_ans = 0.18
            dist_ratio_2_ans = 0.17

            if dist_ratio_1 / dist_ratio_1_ans > 1.4:
                errormsg = errormsg + ("초성의 크기가 너무 커요...\n")
            elif dist_ratio_1 / dist_ratio_1_ans < 0.6:
                errormsg = errormsg + ("초성의 크기가 너무 작아요...\n")

            if dist_ratio_2 / dist_ratio_2_ans > 1.4:
                errormsg = errormsg + ("중성의 크기가 너무 커요...\n")
            elif dist_ratio_2 / dist_ratio_2_ans < 0.6:
                errormsg = errormsg + ("중성의 크기가 너무 작아요...\n")

    if errormsg == "":
        return True, None
    else:
        return False, errormsg
                
