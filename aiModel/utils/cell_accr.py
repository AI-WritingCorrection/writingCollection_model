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
        Cell_1_size = (Cell_1_coord[1][0] - Cell_1_coord[0][0]) * (Cell_1_coord[2][1] - Cell_1_coord[0][1])
        Cell_2_size = (Cell_2_coord[1][0] - Cell_2_coord[0][0]) * (Cell_2_coord[2][1] - Cell_2_coord[0][1])
        Cell_3_size = (Cell_3_coord[1][0] - Cell_3_coord[0][0]) * (Cell_3_coord[2][1] - Cell_3_coord[0][1])

        errormsg = ""

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
        Cell_1_size = (Cell_1_coord[1][0] - Cell_1_coord[0][0]) * (Cell_1_coord[2][1] - Cell_1_coord[0][1])
        Cell_2_size = (Cell_2_coord[1][0] - Cell_2_coord[0][0]) * (Cell_2_coord[2][1] - Cell_2_coord[0][1])

        errormsg = ""
        
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
        return True, None
    else:
        return False, errormsg
                
