from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastApi
from fastapi.middleware.cord import CORSmiddleware

from models import init_db
import requests as rq


@asynccontextmanager
async def lifespan(app_:FastApi):
    await init_db()
    print('Bot is Ready')
    yield



app = FastApi(title="To Do APP",lifespan=lifespan)



app.add_middleware(
    CORSmiddleware,
    allow_origins=['*'],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)



@app.get("/api/tasks/{tg_id}")
async def tasks(tg_id:int):
    user = await rq.add_user(tg_id)
    return await rq.get_tasks(user.id)


@app.get("/api/main/{tg_id}")
async def profile(tg_id:int):
    user  = await rq.add_user(tg_id)
    completed_task_count = await rq.get_compited_tasks_count(user.id)
    return {'completedTasks': completed_task_count}