from uvicorn import run
from fastapi import FastAPI
from project_todo_list.routers import todo_list_router
from shared.exception import NotFound
from shared.exceptions_handler import not_found_exception_handler

app = FastAPI(
    title="DoUp - Lista de Tarefas",
    description="""
    API para gerenciamento de tarefas, fornece endpoints para operações CRUD (Create, Read, Update, Delete), além de um endpoint específico para finalizar tarefas.
    """,
    version="0.1.0",
)

@app.get(
    "/",
    summary="Página inicial da API 'DoUp - Lista de Tarefas'",
)
def todoList() -> str:
    return "DoUp - API para Lista de Tarefas."

app.include_router(todo_list_router.router)
app.add_exception_handler(NotFound, not_found_exception_handler)

if __name__ == "__main__":
    run("main:app",
        host='0.0.0.0',
        port=8000, 
        reload=True)
