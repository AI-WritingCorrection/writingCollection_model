import easyocr
import cv2

def char_read(img_dir):
    reader = easyocr.Reader(['ko'], gpu = False)
    result = reader.readtext(img_dir)
    return result


def bbox_visualization_fullchar(img, result):   #   result는 easyocr 출력값을 기준으로 코딩되어 있음. 수정 필요. 테스트를 위해 get_bbox_smallchar를 사용하려면 [[(리턴값)]] 사용할 것.

    for idx in range(0, len(result)):
        
        TopLeft = result[idx][0][0]
        TopRight = result[idx][0][1]
        BottomLeft = result[idx][0][3]
        BottomRight = result[idx][0][2]

        for x in range(TopLeft[0], TopRight[0]):
            img[TopLeft[1]][x][0] = 128
            img[TopLeft[1]][x][1] = 0
            img[TopLeft[1]][x][2] = 0
            img[BottomLeft[1]][x][0] = 128
            img[BottomLeft[1]][x][1] = 0
            img[BottomLeft[1]][x][2] = 0

        for y in range(TopLeft[1], BottomLeft[1]):
            img[y][TopLeft[0]][0] = 128
            img[y][TopLeft[0]][1] = 0
            img[y][TopLeft[0]][2] = 0
            img[y][TopRight[0]][0] = 128
            img[y][TopRight[0]][1] = 0
            img[y][TopRight[0]][2] = 0

def get_bbox_smallchar(img):

    Top = -1
    Bottom = -1
    Left = -1
    Right = -1

    if img[0][0][0] == 255:    #   이미지가 흰색 배경에 검정 글씨일 때.
        for idx_1 in range(0, len(img)):    #   BottomPixel 찾기
            for idx_2 in range(0, len(img[idx_1])):
                if img[idx_1][idx_2][0] != 255:
                    Bottom = idx_1
                    break

        for idx_1 in range(len(img)-1, -1, -1):     #   TopPixel 찾기
            for idx_2 in range(0, len(img[idx_1])):
                if img[idx_1][idx_2][0] != 255:
                    Top = idx_1
                    break

        for idx_1 in range(0, len(img[0])):     #   RightPixel 찾기
            for idx_2 in range(0, len(img)):
                if img[idx_2][idx_1][0] != 255:
                    Right = idx_1
                    break

        for idx_1 in range(len(img[0])-1, -1, -1):  #    LeftPixel 찾기
            for idx_2 in range(0, len(img)):
                if img[idx_2][idx_1][0] != 255:
                    Left = idx_1

    smallbbox = [[Left, Top], [Right, Top], [Right, Bottom], [Left, Bottom]]

    return smallbbox

def get_bbox_center(bbox):
    Top = bbox[0][1]
    Bottom = bbox[2][1]
    Left = bbox[0][0]
    Right = bbox[1][0]

    center = [round((Top+Bottom) / 2), round((Left+Right) / 2)]
    return center

def dist_smallchar(center1, center2):
    return ((center2[0] - center1[0]) ** 2 + (center2[1] - center1[1]) ** 2) ** 0.5

if __name__=="__main__":
    img_dir = 'img_re.png'   #이미지 디렉토리 입력
    img = cv2.imread(img_dir)

    result = char_read(img_dir)
    
    ans = bboxtest.get_bbox_smallchar(img)
    bboxtest.bbox_visualization_fullchar(img, [[ans]])

    center = bboxtest.get_bbox_center(ans)
    img[center[0]][center[1]][0] = 255
    img[center[0]][center[1]][1] = 255
    img[center[0]][center[1]][2] = 0
                
    cv2.imshow('img', img)
    print(bboxtest.get_bbox_center(ans))
