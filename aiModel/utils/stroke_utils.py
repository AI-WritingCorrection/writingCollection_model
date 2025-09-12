def _xy(p):
    """
    다양한 포인트 표현을 (x, y) 튜플로 표준화한다.
    지원:
      - dict: {"x": float, "y": float}
      - 시퀀스: (x, y) / [x, y]
      - 속성: p.x, p.y  (예: Offset)
    """
    # dict 스타일
    if isinstance(p, dict):
        return float(p["x"]), float(p["y"])
    # 시퀀스 (tuple/list)
    if isinstance(p, (tuple, list)) and len(p) >= 2:
        return float(p[0]), float(p[1])
    # 속성 접근 (Offset 등)
    if hasattr(p, "x") and hasattr(p, "y"):
        return float(getattr(p, "x")), float(getattr(p, "y"))
    raise TypeError(f"Unsupported point type for {_safe_repr(p)}")

def _safe_repr(p, maxlen=120):
    s = repr(p)
    return s if len(s) <= maxlen else s[:maxlen] + "…"

STROKE_DIRECTION_RULES = {
 'ㄱ': {1: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㄲ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'}, 2: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㄳ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'},
       2: {'DELTA_X': '-', 'DELTA_Y': '+'},
       3: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㄴ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㄵ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'},
       2: {'DELTA_X': None, 'DELTA_Y': '+'},
       3: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㄶ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'},
       2: {'DELTA_X': None, 'DELTA_Y': None},
       3: {'DELTA_X': None, 'DELTA_Y': None},
       4: {'DELTA_X': None, 'DELTA_Y': None}},
 'ㄷ': {1: {'DELTA_X': '+', 'DELTA_Y': None}, 2: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㄸ': {1: {'DELTA_X': '+', 'DELTA_Y': None},
       2: {'DELTA_X': '+', 'DELTA_Y': '+'},
       3: {'DELTA_X': '+', 'DELTA_Y': None},
       4: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㄹ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㄺ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': '+', 'DELTA_Y': '+'},
       4: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㄻ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': '+', 'DELTA_Y': '+'},
       4: {'DELTA_X': None, 'DELTA_Y': '+'},
       5: {'DELTA_X': '+', 'DELTA_Y': '+'},
       6: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㄽ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': '+', 'DELTA_Y': '+'},
       4: {'DELTA_X': '-', 'DELTA_Y': '+'},
       5: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㄾ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': '+', 'DELTA_Y': '+'},
       4: {'DELTA_X': '+', 'DELTA_Y': None},
       5: {'DELTA_X': '+', 'DELTA_Y': '+'},
       6: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㄿ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': '+', 'DELTA_Y': '+'},
       4: {'DELTA_X': '+', 'DELTA_Y': None},
       5: {'DELTA_X': None, 'DELTA_Y': '+'},
       6: {'DELTA_X': None, 'DELTA_Y': '+'},
       7: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅀ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': '+', 'DELTA_Y': '+'},
       4: {'DELTA_X': None, 'DELTA_Y': None},
       5: {'DELTA_X': None, 'DELTA_Y': None},
       6: {'DELTA_X': None, 'DELTA_Y': None}},
 'ㅁ': {1: {'DELTA_X': None, 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': '+'},
       3: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅂ': {1: {'DELTA_X': None, 'DELTA_Y': '+'},
       2: {'DELTA_X': None, 'DELTA_Y': '+'},
       3: {'DELTA_X': '+', 'DELTA_Y': None},
       4: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅃ': {1: {'DELTA_X': None, 'DELTA_Y': '+'},
       2: {'DELTA_X': None, 'DELTA_Y': '+'},
       3: {'DELTA_X': '+', 'DELTA_Y': None},
       4: {'DELTA_X': '+', 'DELTA_Y': None},
       5: {'DELTA_X': None, 'DELTA_Y': '+'},
       6: {'DELTA_X': None, 'DELTA_Y': '+'},
       7: {'DELTA_X': '+', 'DELTA_Y': None},
       8: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅄ': {1: {'DELTA_X': None, 'DELTA_Y': '+'},
       2: {'DELTA_X': None, 'DELTA_Y': '+'},
       3: {'DELTA_X': '+', 'DELTA_Y': None},
       4: {'DELTA_X': '+', 'DELTA_Y': None},
       5: {'DELTA_X': '-', 'DELTA_Y': '+'},
       6: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㅅ': {1: {'DELTA_X': '-', 'DELTA_Y': '+'}, 2: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㅆ': {1: {'DELTA_X': '-', 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': '+'},
       3: {'DELTA_X': '-', 'DELTA_Y': '+'},
       4: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㅇ': {1: {'DELTA_X': None, 'DELTA_Y': None}},
 'ㅈ': {1: {'DELTA_X': None, 'DELTA_Y': '+'}, 2: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㅉ': {1: {'DELTA_X': None, 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': '+'},
       3: {'DELTA_X': None, 'DELTA_Y': '+'},
       4: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㅊ': {1: {'DELTA_X': None, 'DELTA_Y': None},
       2: {'DELTA_X': None, 'DELTA_Y': '+'},
       3: {'DELTA_X': '+', 'DELTA_Y': '+'}},
 'ㅋ': {1: {'DELTA_X': '+', 'DELTA_Y': '+'}, 2: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅌ': {1: {'DELTA_X': '+', 'DELTA_Y': None},
       2: {'DELTA_X': '+', 'DELTA_Y': '+'},
       3: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅍ': {1: {'DELTA_X': '+', 'DELTA_Y': None},
       2: {'DELTA_X': None, 'DELTA_Y': '+'},
       3: {'DELTA_X': None, 'DELTA_Y': '+'},
       4: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅎ': {1: {'DELTA_X': None, 'DELTA_Y': None},
       2: {'DELTA_X': None, 'DELTA_Y': None},
       3: {'DELTA_X': None, 'DELTA_Y': None}},
 'ㅏ': {1: {'DELTA_X': None, 'DELTA_Y': '+'}, 2: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅐ': {1: {'DELTA_X': None, 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅑ': {1: {'DELTA_X': None, 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅒ': {1: {'DELTA_X': None, 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': '+', 'DELTA_Y': None},
       4: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅓ': {1: {'DELTA_X': '+', 'DELTA_Y': None}, 2: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅔ': {1: {'DELTA_X': '+', 'DELTA_Y': None},
       2: {'DELTA_X': None, 'DELTA_Y': '+'},
       3: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅕ': {1: {'DELTA_X': '+', 'DELTA_Y': None},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅖ': {1: {'DELTA_X': '+', 'DELTA_Y': None},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': None, 'DELTA_Y': '+'},
       4: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅗ': {1: {'DELTA_X': None, 'DELTA_Y': '+'}, 2: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅘ': {1: {'DELTA_X': None, 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': None, 'DELTA_Y': '+'},
       4: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅚ': {1: {'DELTA_X': None, 'DELTA_Y': '+'},
       2: {'DELTA_X': '+', 'DELTA_Y': None},
       3: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅛ': {1: {'DELTA_X': None, 'DELTA_Y': '+'},
       2: {'DELTA_X': None, 'DELTA_Y': '+'},
       3: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅜ': {1: {'DELTA_X': '+', 'DELTA_Y': None}, 2: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅝ': {1: {'DELTA_X': '+', 'DELTA_Y': None},
       2: {'DELTA_X': None, 'DELTA_Y': '+'},
       3: {'DELTA_X': '+', 'DELTA_Y': None},
       4: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅞ': {1: {'DELTA_X': '+', 'DELTA_Y': None},
       2: {'DELTA_X': None, 'DELTA_Y': '+'},
       3: {'DELTA_X': '+', 'DELTA_Y': None},
       4: {'DELTA_X': None, 'DELTA_Y': '+'},
       5: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅟ': {1: {'DELTA_X': '+', 'DELTA_Y': None},
       2: {'DELTA_X': None, 'DELTA_Y': '+'},
       3: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅠ': {1: {'DELTA_X': '+', 'DELTA_Y': None},
       2: {'DELTA_X': None, 'DELTA_Y': '+'},
       3: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅡ': {1: {'DELTA_X': '+', 'DELTA_Y': None}},
 'ㅢ': {1: {'DELTA_X': '+', 'DELTA_Y': None}, 2: {'DELTA_X': None, 'DELTA_Y': '+'}},
 'ㅣ': {1: {'DELTA_X': None, 'DELTA_Y': '+'}}}





import unicodedata

# 한글 자모 테이블
CHOSUNG_LIST =  ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
                 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
                 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ',
                 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

def decompose_hangul(syllable):
    """한글 음절을 (초성, 중성, 종성) 으로 분해"""
    code = ord(syllable)
    if not (0xAC00 <= code <= 0xD7A3):
        return syllable  # 한글이 아니면 그대로 반환

    base = code - 0xAC00
    cho = base // (21 * 28)
    jung = (base % (21 * 28)) // 28
    jong = base % 28
    return (CHOSUNG_LIST[cho], JUNGSUNG_LIST[jung], JONGSUNG_LIST[jong])


def check_stroke_directions(practice_syllable, stroke_points):
    phonemes = decompose_hangul(practice_syllable)

    expected_directions = []
    for phoneme in phonemes:
        rules = STROKE_DIRECTION_RULES.get(phoneme, {})
        for i in range(1, len(rules) + 1):
            expected_directions.append(rules[i])

    for i, direction in enumerate(expected_directions):
        start = stroke_points[i * 2]
        end = stroke_points[i * 2 + 1]
        sx, sy = _xy(start)
        ex, ey = _xy(end)
        dx, dy = ex - sx, ey - sy

        if direction["DELTA_X"] in ["+", "-"]:
            if (direction["DELTA_X"] == "+" and dx <= 0) or (direction["DELTA_X"] == "-" and dx >= 0):
                return False, f"{i+1}번째 획의 X방향이 {direction['DELTA_X']}이어야 하는데 그렇지 않아요..."

        if direction["DELTA_Y"] in ["+", "-"]:
            if (direction["DELTA_Y"] == "+" and dy <= 0) or (direction["DELTA_Y"] == "-" and dy >= 0):
                return False, f"{i+1}번째 획의 Y방향이 {direction['DELTA_Y']}이어야 하는데 그렇지 않아요..."

    return True, None



##1차 가독성 스테이지 음절 체크 함수

# 1단계 : 문자만 추출하는 함수 정의
def extract_letters(input_string):
  """
  입력된 문자열에서 특수기호, 숫자, 공백을 모두 제거하고
  오직 한글과 영어 알파벳만 남겨서 반환하는 함수
  """
  return "".join([char for char in input_string if char.isalpha()])



# 2단계 : 문자 자모 분리
def separate_jamo(korean_string):
  """
  한글 문자열을 입력받아 초성, 중성, 종성 리스트로 분리하여 반환하는 함수
  """

  # 결과를 담을 리스트 초기화
  chosung_result = []
  jungsung_result = []
  jongsung_result = []

  for char in korean_string:
      # 입력된 문자가 '가'부터 '힣' 사이의 한글 음절인지 확인
      if '가' <= char <= '힣':
            # 한글은 유니코드 값으로 '가'(44032)부터 시작
            # 입력된 글자의 유니코드 값에서 '가'의 값을 빼서 기준을 맞춘다.
            char_code = ord(char) - ord('가')

            # 종성 계산 (총 28개)
            jongseung_index = char_code % 28
            # 중성 계산 (총 21개)
            jungseung_index = (char_code // 28) % 21
            # 초성 계산
            chosung_index = char_code // (28 * 21)

            # 계산된 인덱스로 각 리스트에서 글자를 가져온다.
            chosung_result.append(CHOSUNG_LIST[chosung_index])
            jungsung_result.append(JUNGSUNG_LIST[jungseung_index])

            # 종성은 없는 경우도 있으므로, 빈 문자('')가 아닐 때만 리스트에 추가한다.
            final_consonant = JONGSUNG_LIST[jongseung_index]
            if final_consonant: # final_consonant가 빈 문자가 아니라면
                  jongsung_result.append(final_consonant)
      else:
            # 완성형 글자가 아니면 건너뛴다.
            continue
      

  return chosung_result, jungsung_result, jongsung_result


# 3단계: 가독성 체크 카운트
def count_jamo_matches(sentence, char):
  """
  문장과 글자 하나의 자모를 비교하여 일치하는 자모 종류의 개수를 반환하는 함수
  """
  # 0. 문장에 있을지 모를 특수기호나 공백을 제거한다.
  clean_sentence = extract_letters(sentence)

  # 1. 문장과 글자를 각각 자모 분리한다.
  sent_cho, sent_jung, sent_jong = separate_jamo(clean_sentence)
  char_cho, char_jung, char_jong = separate_jamo(char)

  # 2. 점수를 기록할 변수를 만든다.
  score = 0

  # 3. 자모를 하나씩 비교한다.
  # 초성 비교: 글자의 초성이 문장 초성 리스트에 있는지 확인
  if char_cho and char_cho[0] in sent_cho:
    score += 1

  # 중성 비교: 글자의 중성이 문장 중성 리스트에 있는지 확인
  if char_jung and char_jung[0] in sent_jung:
    score += 1

  # 종성 비교: 글자에 종성이 '있고', 그 종성이 문장 종성 리스트에 있는지 확인
  if char_jong and char_jong[0] in sent_jong:
    score += 1

  # 4. 최종 점수를 반환한다.
  return score


##종성 유무 체크기
def has_jongseung(korean_string):
  """
  입력된 한글 문자열에 종성이 하나라도 있는지 여부를 판단하는 함수
  종성이 있으면 True, 하나도 없으면 False를 반환한다.
  """
  # separate_jamo 함수를 호출해서 초성, 중성, 종성 리스트를 받아온다.
  # 여기서는 종성 리스트만 필요하므로 초성, 중성은 _ 변수로 무시한다.
  _, _, jongseung_list = separate_jamo(korean_string)

  # 종성 리스트에 내용이 있으면 True, 비어있으면 False가 된다.
  return bool(jongseung_list)
