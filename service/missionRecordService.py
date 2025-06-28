from datetime import datetime
from sqlalchemy.orm import Session
from dto.resultDTO import ResultCreate
from domain.missionRecord import MissionRecord

#mission record 객체 생성
def create_mission_record(db: Session, payload: ResultCreate) -> MissionRecord:
    mission_record = MissionRecord(
        user_id=payload.user_id,
        step_id=payload.step_id,  
        isCleared=False, 
        clear_time=None,  
        result=None  
    )

    db.add(mission_record)
    db.commit()
    db.refresh(mission_record)
    return mission_record

# 미션 아이디로 기록 가져오기
def get_mission_record(db: Session, mission_id: int) -> MissionRecord:
    return db.query(MissionRecord).filter(MissionRecord.mission_id == mission_id).first()

# 유저별 기록 가져오기
def get_user_mission_records(db: Session, user_id: int) -> list[MissionRecord]:
    return db.query(MissionRecord).filter(MissionRecord.user_id == user_id).all()

# 기준점수 이상시 미션 클리어 처리
def clear_mission_record(db: Session, mission_id: int) -> MissionRecord:
    mission_record = db.query(MissionRecord).filter(MissionRecord.mission_id == mission_id).first()
    if mission_record:
        mission_record.isCleared = True
        mission_record.clear_time = datetime.now()  # Assuming you want to set the current time as clear time
        db.commit()
        db.refresh(mission_record)
    return mission_record