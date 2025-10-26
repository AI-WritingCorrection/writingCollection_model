from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from domain.missionRecord import MissionRecord
from domain.result import Result
from domain.step import Step
from dto.statsDTO import StatsResponse


def get_user_statistics(db: Session, user_id: int) -> List[StatsResponse]:
    """
    특정 유저의 모든 '제출된' 미션 기록을 통계 DTO 리스트로 반환합니다.

    - MissionRecord: mission_id, isCleared, submission_time
    - Step (JOIN): step_type
    - Result (LEFT OUTER JOIN): score
    """
    
    # 1. DTO에 필요한 컬럼들을 선택하는 쿼리 작성
    query = (
        select(
            MissionRecord.mission_id,
            Step.step_type,
            Result.score,
            MissionRecord.isCleared,
            MissionRecord.submission_time
        )
        # MissionRecord -> Step (INNER JOIN)
        .join(Step, MissionRecord.step_id == Step.step_id)
        # MissionRecord -> Result (LEFT OUTER JOIN)
        # : Result(채점)가 없는 시도(submission)가 있을 수도 있음을 대비
        # : StatsDto의 score가 Optional[int]이므로 OUTER JOIN이 적합
        .outerjoin(Result, MissionRecord.mission_id == Result.mission_id)
        # 2. 특정 유저로 필터링
        .filter(MissionRecord.user_id == user_id)
        # 3. '제출된' 기록만 필터링 (DB 모델 수정 사항 반영)
        .filter(MissionRecord.submission_time.isnot(None))
        # 4. 시간순으로 정렬 (차트 생성 시 기본 정렬)
        .order_by(MissionRecord.submission_time.asc())
    )

    # 5. 쿼리 실행 (결과는 (mission_id, step_type, ...) 형태의 튜플 리스트)
    results_from_db = db.execute(query).all()

    # 6. DB 결과(튜플)를 StatsDto 객체 리스트로 변환
    stats_list = [
        StatsResponse(
            mission_id=row.mission_id,
            step_type=row.step_type,
            score=row.score,
            isCleared=row.isCleared,
            submission_time=row.submission_time
        )
        for row in results_from_db
    ]

    return stats_list