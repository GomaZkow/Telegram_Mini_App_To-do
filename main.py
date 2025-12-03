from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from crud import add_user, get_tasks, get_completed_tasks_count
from models import init_db


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print("Bot is Ready")
    yield


app = FastAPI(title="To Do APP", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/tasks/{tg_id}")
async def tasks(tg_id: int):
    user = await add_user(tg_id)
    return await get_tasks(user.id)


@app.get("/api/main/{tg_id}")
async def profile(tg_id: int):
    user = await add_user(tg_id)
    completed_task_count = await get_completed_tasks_count(user.id)
    return {"completedTasks": completed_task_count}
