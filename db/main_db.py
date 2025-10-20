import sqlite3
from datetime import datetime
from config import path_db  # Пусть здесь путь к вашей базе, например 'todo.db'
from db import queries


def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_TASK)
    print("База данных подключена!")
    conn.commit()
    conn.close()


def add_task(task):
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M')
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASK, (task, time_now))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def get_tasks():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.SELECT_TASK)
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def delete_task(task_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()


def update_task(task_id, new_task):
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M')
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.UPDATE_TASK, (new_task, time_now, task_id))
    conn.commit()
    conn.close()

def delete_all_tasks():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_ALL_TASKS)
    conn.commit()
    conn.close()



