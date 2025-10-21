from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.practice import Practice
from domain.missionRecord import MissionRecord
from domain.step import Step
from dto.StepSchema import StepSchema
from dto.PracticeSchema import PracticeSchema
from dto.missionRecordSchema import MissionRecordSchema


router=APIRouter()

# DB에서 step 리스트를 가져오는 함수
@router.get("/step", response_model=List[StepSchema])
def get_step_list_from_db(db: Session = Depends(get_db)):

    try:
        steps = db.query(Step).order_by(Step.step_id.asc()).all()
        return steps
    except Exception as e:
        print(f"Error fetching steps from database: {e}")
        return []

# DB에서 practice 리스트를 가져오는 함수
@router.get("/practice", response_model=List[PracticeSchema])
def get_practice_list_from_db(db: Session = Depends(get_db)):

    try:
        practices = db.query(Practice).order_by(Practice.practice_id.asc()).all()
        return practices
    except Exception as e:
        print(f"Error fetching practices from database: {e}")
        return []
    

# Fetch mission records by user_id
@router.get("/missionrecords/{user_id}", response_model=List[MissionRecordSchema])
def get_mission_records_for_user(user_id: int, db: Session = Depends(get_db)):
    """
    특정 user_id에 해당하는 mission record 리스트를 반환합니다.
    """
    try:
        records = (
            db.query(MissionRecord)
              .filter(MissionRecord.user_id == user_id)
              .order_by(MissionRecord.step_id.asc())
              .all()
        )
        return records
    except Exception as e:
        print(f"Error fetching mission records for user {user_id}: {e}")
        return []

