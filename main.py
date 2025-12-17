from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_db  
from requests import (
    add_user,
    get_tasks,
    get_completed_tasks_count,
    add_task,
    update_task,
)

from pydantic import BaseModel

class AddTask(BaseModel):
    tg_id: int
    title: str

class CompleteTask(BaseModel):
    id: int

app = FastAPI(title="To Do APP")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #не забыть поменять на онли запрос с фронта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/api/tasks/{tg_id}")
async def tasks(tg_id: int):
    user = await add_user(tg_id)
    result = await get_tasks(user.id)
    return result

@app.get("/api/main/{tg_id}")
async def profile(tg_id: int):
    user = await add_user(tg_id)
    completed_task_count = await get_completed_tasks_count(user.id)
    return {"completedTasks": completed_task_count}

@app.post("/api/add")
async def add_task_endpoint(task: AddTask):
    user = await add_user(task.tg_id)
    await add_task(user.id, task.title)
   
    completed_task_count = await get_completed_tasks_count(user.id)#отдаю ирл счетчик
    return {"status": "ok", "completedTasks": completed_task_count}

@app.patch("/api/completed")
async def complete_task_endpoint(task: CompleteTask):
    completed_count = await update_task(task.id)
    return {"completedTasks": completed_count}
