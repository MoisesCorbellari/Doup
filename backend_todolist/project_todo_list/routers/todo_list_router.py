from fastapi import APIRouter, Depends, HTTPException
from shared.dependencies import get_db
from sqlalchemy.orm import Session
from project_todo_list.models.todo_list_model import DoUp
from typing import List
from shared.exception import NotFound
from project_todo_list.schemas.schema import ToDoListRequest, ToDoListResponse

router = APIRouter(prefix='/DoUp', tags=["Lista de tarefas"])

def find_todolist_by_id(id_task: int, db: Session) -> DoUp:
    todo_list = db.get(DoUp, id_task)
    if todo_list is None:
        raise NotFound(name="")
    
    return todo_list

#endpoint para obter todas as tarefas
@router.get("/get-all", response_model=List[ToDoListResponse])
def get_all_todo_list(db: Session = Depends(get_db)) -> List[ToDoListResponse]:
    return db.query(DoUp).all()

#endpoint para obter tarefas por id
@router.get("/get-by-id/{id_task}", response_model=ToDoListResponse)
def get_todo_list_by_id(id_task: int,
                        db: Session = Depends(get_db)) -> List[ToDoListResponse]:
    todo_list: DoUp = find_todolist_by_id(id_task, db)
    return todo_list

#endpoint para criar tarefas
@router.post("/create", response_model=ToDoListResponse, status_code=201)
def create_todo_list(task_request: ToDoListRequest,
                     db: Session = Depends(get_db)) -> ToDoListResponse:

    todo_list = DoUp(
        **task_request.model_dump() 
    )
    
    db.add(todo_list) 
    db.commit() 
    db.refresh(todo_list) 
    return todo_list 

#endpoint para atualizar tarefas
@router.put("/update/{id_task}", response_model=ToDoListResponse, status_code=200)
def update_todo_list_by_id(id_task: int,
                            task_request: ToDoListRequest,
                            db: Session = Depends(get_db)) -> ToDoListResponse:
    todo_list = find_todolist_by_id(id_task, db)
    
    todo_list.title = task_request.title
    todo_list.description = task_request.description
    todo_list.completed = task_request.completed
    
    db.add(todo_list)
    db.commit()
    db.refresh(todo_list)
    return todo_list

#endpoint para finalizar tarefas
@router.post("/finish/{id_task}", response_model=ToDoListResponse, status_code=200)
def finish_todo_list_by_id(id_task: int, db: Session = Depends(get_db)) -> ToDoListResponse:
    todo_list = find_todolist_by_id(id_task, db)

    if todo_list.completed:
        raise HTTPException(status_code=400, detail="Tarefa já foi finalizada!")

    todo_list.completed = True
    
    db.add(todo_list)
    db.commit()
    db.refresh(todo_list)
    return todo_list

#endpoint para apagar tarefas
@router.delete("/delete/{id_task}", status_code=204)
def delete_todo_list_by_id(id_task: int,
                     db: Session = Depends(get_db)) -> None:
    todo_list = find_todolist_by_id(id_task, db)

    db.delete(todo_list)
    db.commit()


