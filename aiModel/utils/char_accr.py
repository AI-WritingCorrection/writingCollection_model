import numpy as np

from .bboxtest import get_bbox_smallchar

def check_char_size(images):

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
