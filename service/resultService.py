from sqlalchemy.orm import Session
from domain.result import Result

def create_result(db: Session, mission_id: int, score: int) -> Result:
    result = Result(
        mission_id=mission_id,
        score=score,
    )
    
    db.add(result)
    db.commit()
    db.refresh(result)
    return result