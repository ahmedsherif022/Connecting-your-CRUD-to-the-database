from fastapi import  FastAPI, HTTPException, Response
from streamlit import title
from pydantic import BaseModel

import sqlite3

DB_PATH = "tasks.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # so rows behave like dicts
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN DEFAULT 0
        )
    """)
    # Seed only if empty
    count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [("Learn SQL", 0), ("Build CRUD API", 1), ("Connect database", 0)]
        )
        conn.commit()
    conn.close()

init_db()  # runs once when the app starts

class TaskCreate(BaseModel):
    title: str


app=FastAPI(
     title='task api',
     version='1.0.0',
 )

# tasks = [
#     {"id": 1, "title": "Buy milk", "done": False},
#     {"id": 2, "title": "Write report", "done": False},
#     {"id": 3, "title": "Call mom", "done": True},
# ]



@app.get('/')
def root():
    return {
         'name': 'task api',
         'version': '1.0.0',
         'endpoints':{
             'list_tasks':'Get /tasks',
             'get_tasks': 'Get /tasks/{id}',
             'create_task': 'Post /tasks',
             'update_task': 'Put /tasks/{id}',
             'delete_task': 'Delete /tasks/{id}',
            
         },
     }
    
# @app.get('/health')
# def health():
#     return {'status': 'ok'}

# @app.get('/tasks', summary="List all tasks")
# def list_tasks():
#     return tasks

# @app.get('/tasks/{task_id}', summary="Get one task by ID")
# def get_task(task_id:int):
#     for task in tasks :
#         if task['id'] == task_id:
#             return task
#         raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
# @app.post('/tasks',status_code=201,summary="Create a new task")
# def create_task(body:TaskCreate):
#     if not body.title.strip():
#         raise HTTPException(status_code=400, detail="Title cannot be empty")
#     new_id=max((t['id']for t in tasks), default=0)+1
#     tasks.append({'id':new_id, 'title':body.title, 'done':False})
#     return tasks

# class TaskUpdate(BaseModel):
#     title: str | None = None
#     done: bool | None = None

# @app.put('/tasks/{task_id}', summary="Update an existing task")
# def update_task(task_id:int,body:TaskUpdate):
#     for task in tasks :
#         if task['id']==task_id:
#             if body.title is not None:
#                 if not body.title.strip():
#                     raise HTTPException(status_code=400, detail="Title cannot be empty")
#                 task['title']=body.title.strip()
#             if body.done is not None:
#                 task['done']=body.done
#             return task
#     raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

# @app.delete('/tasks/{task_id}',status_code=204, summary="Delete a task")
# def delete_task(task_id:int):
#     for i , task in enumerate(tasks):
#         if task['id']==task_id:
#             del tasks[i]
#             return Response(status_code=204)
#     raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

# using database  ---------------------------------------------------------------------------------------------

@app.get('/tasks', summary="List all tasks from database")     
def get_tasks_db():
    conn =get_db()
    rows=conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get('/tasks/{task_id}', summary="Get one task by ID from database")
def get_task_db(task_id:int):
    conn= get_db()
    row=conn.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return dict(row)

@app.post('/tasks',status_code=201,summary="Create a new task in database")
def create_task(body:TaskCreate):
    if not body.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    conn=get_db()
    cursor=conn.execute('INSERT INTO tasks (title,done) VALUES (?,?)', (body.title.strip(), 0))
    conn.commit()
    new_id=cursor.lastrowid
    conn.close()
    return {'id':new_id, 'title':body.title, 'done':False}
    

@app.put("/tasks/{task_id}")
def update_task(task_id: int, body: TaskCreate):
    conn = get_db()

    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if row is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    title = body.title if body.title is not None else row["title"]
    done = body.done if body.done is not None else row["done"]

    conn.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (title, done, task_id)
    )

    conn.commit()
    conn.close()

    return {
        "id": task_id,
        "title": title,
        "done": done
    }
    
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    conn = get_db()

    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if row is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return Response(status_code=204)
