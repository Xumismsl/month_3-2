import sqlite3
from datetime import datetime
from config import path_db
from db import queries


def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_TASK)
    conn.commit()
    conn.close()
    print("База данных подключена!")


def add_task(task):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASK, (task, 0, time_now))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def get_tasks(filter_type='all'):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if filter_type == 'completed':
        cursor.execute(queries.SELECT_TASKS_COMPLETED)
    elif filter_type == 'uncompleted':
        cursor.execute(queries.SELECT_TASKS_UNCOMPLETED)
    else:
        cursor.execute(queries.SELECT_TASK)
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task(task_id, new_task):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.UPDATE_TASK, (new_task, time_now, task_id))
    conn.commit()
    conn.close()


def update_task_status(task_id, completed):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.UPDATE_TASK_STATUS, (completed, task_id))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()


def delete_all_tasks():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_ALL_TASKS)
    conn.commit()
    conn.close()
