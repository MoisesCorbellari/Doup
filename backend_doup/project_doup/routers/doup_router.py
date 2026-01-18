from fastapi import APIRouter, Depends, HTTPException
from shared.dependencies import get_db
from sqlalchemy.orm import Session
from project_doup.models.doup_model import DoUp
from typing import List
from shared.exception import NotFound
from project_doup.schemas.schema import DoUpRequest, DoUpResponse

router = APIRouter(prefix='/DoUp', tags=["Lista de tarefas"])

def find_task_by_id(id_task: int, db: Session) -> DoUp:
    task = db.get(DoUp, id_task)
    if task is None:
        raise NotFound(name="")
    
    return task

#endpoint para obter todas as tarefas
@router.get("/get-all", response_model=List[DoUpResponse])
def get_all_task(db: Session = Depends(get_db)) -> List[DoUpResponse]:
    return db.query(DoUp).all()

#endpoint para obter tarefas por id
@router.get("/get-by-id/{id_task}", response_model=DoUpResponse)
def get_task_by_id(id_task: int,
                        db: Session = Depends(get_db)) -> List[DoUpResponse]:
    task: DoUp = find_task_by_id(id_task, db)
    return task

#endpoint para criar tarefas
@router.post("/create", response_model=DoUpResponse, status_code=201)
def create_task(task_request: DoUpRequest,
                     db: Session = Depends(get_db)) -> DoUpResponse:

    task = DoUp(
        **task_request.model_dump() 
    )
    
    db.add(task) 
    db.commit() 
    db.refresh(task) 
    return task 

#endpoint para atualizar tarefas
@router.put("/update/{id_task}", response_model=DoUpResponse, status_code=200)
def update_task_by_id(id_task: int,
                            task_request: DoUpRequest,
                            db: Session = Depends(get_db)) -> DoUpResponse:
    task = find_task_by_id(id_task, db)
    
    task.title = task_request.title
    task.description = task_request.description
    task.completed = task_request.completed
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

#endpoint para finalizar tarefas
@router.post("/finish/{id_task}", response_model=DoUpResponse, status_code=200)
def finish_task_by_id(id_task: int, db: Session = Depends(get_db)) -> DoUpResponse:
    task = find_task_by_id(id_task, db)

    if task.completed:
        raise HTTPException(status_code=400, detail="Tarefa já foi finalizada!")

    task.completed = True
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

#endpoint para apagar tarefas
@router.delete("/delete/{id_task}", status_code=204)
def delete_task_by_id(id_task: int,
                     db: Session = Depends(get_db)) -> None:
    task = find_task_by_id(id_task, db)

    db.delete(task)
    db.commit()


