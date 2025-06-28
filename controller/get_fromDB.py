from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.practice import Practice
from domain.step import Step
from dto.StepSchema import StepSchema
from dto.PracticeSchema import PracticeSchema


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