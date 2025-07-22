from fastapi import APIRouter, Depends, HTTPException
from app.db.schemas import ApplicationBase, ApplicationCreate, ApplicationUpdate
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[ApplicationBase])
def list_applications(db=Depends(get_db)):
    return db.query(ApplicationBase).all(), 200

@router.get("/{application_id}", response_model=ApplicationBase)
def get_application(application_id: int, db=Depends(get_db)):
    application = db.query(ApplicationBase).get(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application, 200

@router.post("/", response_model=ApplicationBase)
def create_application(application: ApplicationCreate, db=Depends(get_db)):
    db_application = ApplicationBase(**application.model_dump())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application, 201

@router.put("/{application_id}", response_model=ApplicationBase)
def update_application(application_id: int, application: ApplicationUpdate, db=Depends(get_db)):
    db_application = db.query(ApplicationBase).get(application_id)
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    for field, value in application.model_dump(exclude_unset=True).items():
        setattr(db_application, field, value)
    db.commit()
    db.refresh(db_application)
    return db_application, 200

@router.delete("/{application_id}", status_code=204)
def delete_application(application_id: int, db=Depends(get_db)):
    db_application = db.query(ApplicationBase).get(application_id)
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(db_application)
    db.commit()
    return {"message": "Application deleted successfully"}, 204
    
    