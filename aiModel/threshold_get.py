from utils.bboxtest import get_bbox_smallchar

import cv2

file_dir = "Threshold\\7"

char_dir = file_dir + "\\Full_Shot\\char.png"
Cell_1_dir = file_dir + "\\Segment\\Cell_1.png"
Cell_2_dir = file_dir + "\\Segment\\Cell_2.png"
Cell_3_dir = file_dir + "\\Segment\\Cell_3.png"

char = cv2.imread(char_dir)
Cell_1 = cv2.imread(Cell_1_dir)
Cell_2 = cv2.imread(Cell_2_dir)


char_coord = get_bbox_smallchar(char)
Cell_1_coord = get_bbox_smallchar(Cell_1)
Cell_2_coord = get_bbox_smallchar(Cell_2)


char_size = (char_coord[1][0] - char_coord[0][0]) * (char_coord[2][1] - char_coord[0][1])
Cell_1_size = (Cell_1_coord[1][0] - Cell_1_coord[0][0]) * (Cell_1_coord[2][1] - Cell_1_coord[0][1])
Cell_2_size = (Cell_2_coord[1][0] - Cell_2_coord[0][0]) * (Cell_2_coord[2][1] - Cell_2_coord[0][1])


print("char_size : " + str(char_size))
print("Cell_1_size : " + str(Cell_1_size))
print("Cell_2_size : " + str(Cell_2_size))


Cell_1_ratio = Cell_1_size / char_size
Cell_2_ratio = Cell_2_size / char_size



print("Cell_1_ratio : " + str(Cell_1_ratio))
print("Cell_2_ratio : " + str(Cell_2_ratio))



Cell_3 = cv2.imread(Cell_3_dir)
Cell_3_coord = get_bbox_smallchar(Cell_3)
Cell_3_size = (Cell_3_coord[1][0] - Cell_3_coord[0][0]) * (Cell_3_coord[2][1] - Cell_3_coord[1][1])
print("Cell_3_size : " + str(Cell_3_size))
Cell_3_ratio = Cell_3_size / char_size
print("Cell_3_ratio : " + str(Cell_3_ratio))
