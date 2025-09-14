from PIL import Image
import io
import base64
from typing import List

#이미지 병합 함수 (획 => 한글자)
def merge_images(images):
    """
    images: 병합할 PIL.Image 객체들의 리스트
            (예: 하나의 글자를 구성하는 여러 획 이미지)

    return: 병합된 이미지의 PNG 포맷 byte 값
            → OCR, 저장 등 용도에 사용 가능
    """
    base_image = None
    for img in images:
        img = img.convert("RGBA")  # 혹시 RGB인 이미지가 섞여 있을 경우 대비
        if base_image is None:
            base_image = Image.new("RGBA", img.size, (255, 255, 255, 255))  # 흰색 배경
        base_image = Image.alpha_composite(base_image, img)

    # PNG 바이트로 저장
    img_io = io.BytesIO()
    base_image.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io.getvalue()



def split_and_merge_images(files, chunk_sizes):
    """
    files: 이미지 파일 리스트
    chunk_sizes: 각 묶음의 크기를 지정하는 리스트 (예: [5, 3, 3])
    return: 병합된 이미지들의 byte 리스트 [5개병합, 3개병합, 3개병합] or [5개병합, 2개병합]
    """
    results = []
    start = 0

    for size in chunk_sizes:
        if size <= 0:
            continue  # 0 이하 크기는 무시

        end = start + size
        chunk = files[start:end]
        if not chunk:
            break  # 남은 파일이 없으면 종료

        merged_bytes = merge_images(chunk)
        results.append(merged_bytes)
        start = end

    return results


def prepare_images_for_check(img_tot_bytes, stroke_images, stroke_counts):
    """
    사용자의 원본 데이터들을 get_char_acc_new 함수가 요구하는 형식으로 변환한다.

    Args:
        img_tot_bytes (bytes): 완성된 전체 글자의 PNG 바이트
        stroke_images (list): 개별 획 이미지 리스트 (PIL.Image 객체 등)
        chunk_sizes (list): 초성, 중성, 종성을 구성하는 획의 개수 (예: [2, 2, 2])

    Returns:
        list: [전체글자, 초성, 중성, 종성] 순서의 PIL.Image 객체 리스트
    """
    
    # --- 내부 헬퍼 함수: 바이트를 PIL 이미지로 변환 ---
    def _bytes_to_pil(image_bytes):
        return Image.open(io.BytesIO(image_bytes))

    # --- 1. 전체 글자 이미지 준비 ---
    full_char_image = _bytes_to_pil(img_tot_bytes)
    
    # --- 2. 초성, 중성, 종성 이미지 준비 ---
    # (1) 획들을 합쳐 자/모음 이미지의 '바이트' 리스트를 생성
    jamo_bytes_list = split_and_merge_images(stroke_images, stroke_counts)
    
    # (2) '바이트' 리스트를 'PIL 이미지' 리스트로 변환
    jamo_image_list = [_bytes_to_pil(b) for b in jamo_bytes_list]
    
    # --- 3. 최종 리스트 완성 ---
    # [전체글자_이미지] + [초성_이미지, 중성_이미지, ...]
    final_image_list = [full_char_image] + jamo_image_list
    
    return final_image_list


# Base64 → PIL.Image 객체로 변환
def decode_base64_image_list(base64_list: list) -> List[Image.Image]:
    """
    Base64 인코딩된 이미지 문자열 리스트를 PIL 이미지 객체 리스트로 변환하는 함수

    Args:
        base64_list (list): 하나의 셀에 해당하는 Base64 문자열 리스트

    Returns:
        list: 변환된 PIL.Image 객체 리스트
    """
    image_list = []

    for idx, b64_str in enumerate(base64_list):
        try:
            img_data = base64.b64decode(b64_str)
            img = Image.open(io.BytesIO(img_data)).convert("RGBA")
            image_list.append(img)
        except Exception as e:
            print(f"❌ 에러 - 이미지 {idx}: {e}")

    return image_list


