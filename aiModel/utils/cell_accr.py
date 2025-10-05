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
    last_is_null = False
    
    char_decom = char_decompose(practice_syllabus)

    if char_decom[0][2] == '':
        last_is_null = True
        char_type = CHAR_TYPE_RULES[char_decom[0][1]]
    else:
        char_type = CHAR_TYPE_RULES[char_decom[0][1]]
        
    if last_is_null == False:
        
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

        if char_type == 0:
            #   사이즈에 대한 오류를 에러 코드로 표시한 후, return하고 한 번에 출력하는 것은 어떤가?
            Cell_ratio_1_ans = 0.2813292884721456
            Cell_ratio_2_ans = 0.2124931053502482
            Cell_ratio_3_ans = 0.2214561500275786

                
        elif char_type == 1:
            
            Cell_ratio_1_ans = 0.34016940109377086
            Cell_ratio_2_ans = 0.27611044417767105
            Cell_ratio_3_ans = 0.2702080832332933

        elif char_type == 2:
            
            Cell_ratio_1_ans = 0.23140671483212918
            Cell_ratio_2_ans = 0.2967032967032967
            Cell_ratio_3_ans = 0.3183777548418432

        elif char_type == 3:
            
            Cell_ratio_1_ans = 0.24609920466274057
            Cell_ratio_2_ans = 0.6538461538461539
            Cell_ratio_3_ans = 0.23878331613138243

        elif char_type == 4:
            
            Cell_ratio_1_ans = 0.2636893799877225
            Cell_ratio_2_ans = 0.08888888888888889
            Cell_ratio_3_ans = 0.24843462246777165

        elif char_type == 5:
            
            Cell_ratio_1_ans = 0.351661610590182
            Cell_ratio_2_ans = 0.111003861003861
            Cell_ratio_3_ans = 0.27682018753447324

        elif char_type == 6:
            
            Cell_ratio_1_ans = 0.28768624014022787
            Cell_ratio_2_ans = 0.24536747214223112
            Cell_ratio_3_ans = 0.24668210842619256

        elif char_type == 7:
            
            Cell_ratio_1_ans = 0.28768624014022787
            Cell_ratio_2_ans = 0.33150744960560913
            Cell_ratio_3_ans = 0.24668210842619256

        elif char_type == 8:
            
            Cell_ratio_1_ans = 0.19102835939570634
            Cell_ratio_2_ans = 0.5969387755102041
            Cell_ratio_3_ans = 0.2500662602703419

        elif char_type == 9:
            
            Cell_ratio_1_ans = 0.1989795918367347
            Cell_ratio_2_ans = 0.6428571428571429
            Cell_ratio_3_ans = 0.26672152732060567
            
        elif char_type == 10:
            
            Cell_ratio_1_ans = 0.17007839721254356
            Cell_ratio_2_ans = 0.6326530612244898
            Cell_ratio_3_ans = 0.642297162767546

        elif char_type == 11:
            
            Cell_ratio_1_ans = 0.1394453486916239
            Cell_ratio_2_ans = 0.6071428571428571
            Cell_ratio_3_ans = 0.23278452485288595
            
        elif char_type == 12:
            
            Cell_ratio_1_ans = 0.17447679708826205
            Cell_ratio_2_ans = 0.6275510204081632
            Cell_ratio_3_ans = 0.23446639802417782

        elif char_type == 13:
            
            Cell_ratio_1_ans = 0.15816326530612246
            Cell_ratio_2_ans = 0.6071428571428571
            Cell_ratio_3_ans = 0.2021615097651964

        elif char_type == 14:
            
            Cell_ratio_1_ans = 0.18979591836734694
            Cell_ratio_2_ans = 0.6632653061224489
            Cell_ratio_3_ans = 0.24479921000658328
            
        if Cell_1_size / char_size > Cell_ratio_1_ans * 1.3:
            errormsg = errormsg + ("첫 번째 글자의 크기가 너무 커요...\n")
        elif Cell_1_size / char_size < Cell_ratio_1_ans * 0.7:
            errormsg = errormsg + ("첫 번째 글자의 크기가 너무 작아요...\n")

        if Cell_2_size / char_size > Cell_ratio_2_ans * 1.3:
            errormsg = errormsg + ("두 번째 글자의  크기가 너무 커요...\n")
        elif Cell_2_size / char_size < Cell_ratio_2_ans * 0.7:
            errormsg = errormsg + ("두 번째 글자의 크기가 너무 작아요...\n")

        if Cell_3_size / char_size > Cell_ratio_3_ans * 1.3:
            errormsg = errormsg + ("세 번째 글자의 크기가 너무 커요...\n")
        elif Cell_3_size / char_size < Cell_ratio_3_ans * 0.7:
            errormsg = errormsg + ("세 번째 글자의 크기가 너무 작아요...\n")
            
        
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
            #   사이즈에 대한 오류를 에러 코드로 표시한 후, return하고 한 번에 출력하는 것은 어떤가?
            Cell_ratio_1_ans = 0.32366723634158445
            Cell_ratio_2_ans = 0.36363636363636365

                
        elif char_type == 1:
            
            Cell_ratio_1_ans = 0.39302450127192395
            Cell_ratio_2_ans = 0.4805194805194805

        elif char_type == 2:
            
            Cell_ratio_1_ans = 0.49974164314956876
            Cell_ratio_2_ans = 0.5611510791366906

        elif char_type == 3:
            
            Cell_ratio_1_ans = 0.3153516667701285
            Cell_ratio_2_ans = 0.5730337078651685

        elif char_type == 4:
            
            Cell_ratio_1_ans = 0.5494616284227931
            Cell_ratio_2_ans = 0.11678832116788321

        elif char_type == 5:
                        
            Cell_ratio_1_ans = 0.40350515463917525
            Cell_ratio_2_ans = 0.18666666666666668

        elif char_type == 6:
                        
            Cell_ratio_1_ans = 0.30639687520010245
            Cell_ratio_2_ans = 0.43478260869565216

        elif char_type == 7:
            
            Cell_ratio_1_ans = 0.30639687520010245
            Cell_ratio_2_ans = 0.5652173913043478

        elif char_type == 8:
            
            Cell_ratio_1_ans = 0.24675324675324675
            Cell_ratio_2_ans = 1.0  

        elif char_type == 9:
            
            Cell_ratio_1_ans = 0.23870967741935484
            Cell_ratio_2_ans = 1.0

        elif char_type == 10:
            
            Cell_ratio_1_ans = 0.16237113402061856
            Cell_ratio_2_ans = 1.0

        elif char_type == 11:
                        
            Cell_ratio_1_ans = 0.1806337360065777
            Cell_ratio_2_ans = 1.0

        elif char_type == 12:
            
            Cell_ratio_1_ans = 0.2229299363057325
            Cell_ratio_2_ans = 1.0

        elif char_type == 13:
            
            Cell_ratio_1_ans = 0.20219487861656135
            Cell_ratio_2_ans = 1.0

        elif char_type == 14:
            
            Cell_ratio_1_ans = 0.22903225806451613
            Cell_ratio_2_ans = 1.0
            
        if Cell_1_size / char_size > Cell_ratio_1_ans * 1.3:
            errormsg = errormsg + ("첫 번째 글자의 크기가 너무 커요...\n")
        elif Cell_1_size / char_size < Cell_ratio_1_ans * 0.7:
            errormsg = errormsg + ("첫 번째 글자의 크기가 너무 작아요...\n")

        if Cell_2_size / char_size > Cell_ratio_2_ans * 1.3:
            errormsg = errormsg + ("두 번째 글자의  크기가 너무 커요...\n")
        elif Cell_2_size / char_size < Cell_ratio_2_ans * 0.7:
            errormsg = errormsg + ("두 번째 글자의 크기가 너무 작아요...\n")

                
    if errormsg == "":
        return True, None
    else:
        return False, errormsg
                
