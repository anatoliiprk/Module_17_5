from fastapi import FastAPI
from app.routers.task import router_task
from app.routers.user import router_user

app = FastAPI()


@app.get('/')
async def welcome():
    return {'message': 'Welcome to Taskmanager'}


app.include_router(router_task)
app.include_router(router_user)
