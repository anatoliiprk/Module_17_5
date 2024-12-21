from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router_task = APIRouter(prefix='/task', tags=['task'])


@router_task.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router_task.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    else:
        return task


@router_task.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_new_task: CreateTask, id_user: int):
    db.execute(insert(Task).values(title=create_new_task.title,
                                   content=create_new_task.content,
                                   priority=create_new_task.priority,
                                   user_id=id_user,
                                   slug=slugify(create_new_task.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router_task.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask):
    task = db.scalars(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    else:
        db.execute(update(Task).where(Task.id == task_id).values(title=update_task.title,
                                                                 content=update_task.content,
                                                                 priority=update_task.priority,
                                                                 slug=slugify(update_task.username)))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful!'
        }


@router_task.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalars(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    else:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User delete is successful!'
        }
