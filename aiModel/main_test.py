import base64
from PIL import Image
import io
import os
import numpy as np

from utils.image_utils import merge_images
from utils.image_utils import decode_base64_image_list

from utils.font_score_utils import evaluate_character

image_paths = [
    "checking_file\\Full_Shot\\char.png",
    "checking_file\\Segment\\Cell_1.png",
    "checking_file\\Segment\\Cell_2.png",
    "checking_file\\Segment\\Cell_3.png"
]

base64_images = []
for img_path in image_paths:
    with open(img_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        base64_images.append(encoded)

images = decode_base64_image_list(base64_images)
img_bytes = merge_images(images)

sample_data = {
    "user_id": "user123",
    "practice_text": "감",
    "cellImages": {
        "0": base64_images
    },
    "detailedStrokeCounts": {
        "0": [1, 2, 3]
    },
  "firstAndLastStroke": {
      "0": [
    {"x": 10, "y": 10}, {"x": 20, "y": 20},   # ㄱ: ↘ (OK)
    {"x": 30, "y": 10}, {"x": 30, "y": 40},   # ㅏ: 세로 (OK)
    #{"x": 60, "y": 40}, {"x": 30, "y": 40},   # ❌ ㅏ: 가로 (거꾸로 ← 방향 오류!)
    {"x": 30, "y": 40}, {"x": 60, "y": 40},   # ❌ ㅏ: 가로 (거꾸로 ← 방향 오류!)->테스트를 위해 고쳤어요
    {"x": 70, "y": 10}, {"x": 70, "y": 40},   # ㅁ: 세로 (OK)
    {"x": 70, "y": 40}, {"x": 90, "y": 60},   # ㅁ: ↘ (OK)
    {"x": 90, "y": 60}, {"x": 120, "y": 60},  # ㅁ: 가로 (OK)
]
  }
}

stroke_counts = sample_data["detailedStrokeCounts"]["0"]
stroke_points = sample_data["firstAndLastStroke"]["0"]
practice_syllabus = sample_data["practice_text"]

score_result = evaluate_character(images, stroke_counts, stroke_points, practice_syllabus)

print("Error Stage : " + score_result["stage"])
print("Reason : ")
print(score_result["reason"])
print("Score : " + str(score_result["score"]))
