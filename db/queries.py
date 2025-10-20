CREATE_TABLE_TASK = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        Time TEXT
    )
"""

INSERT_TASK = 'INSERT INTO tasks (task, Time) VALUES (?, ?)'

SELECT_TASK = "SELECT id, task, Time FROM tasks"

UPDATE_TASK = "UPDATE tasks SET task = ?, Time = ? WHERE id = ?"

DELETE_TASK = 'DELETE FROM tasks WHERE id = ?'
DELETE_ALL_TASKS = "DELETE FROM tasks"
