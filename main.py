from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import sqlite3, uuid

# ---------------------------
# Inicialización de FastAPI
# ---------------------------
app = FastAPI()

# CORS: permitir tu dominio de GitHub Pages
origins = ["https://lucasmiguelsant.github.io"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Modelo de tarea
# ---------------------------
class Task(BaseModel):
    id: str | None = None
    title: str
    note: str | None = None
    datetime: datetime
    status: str = "pending"

# ---------------------------
# Inicializar DB SQLite
# ---------------------------
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT,
    note TEXT,
    datetime TEXT,
    status TEXT,
    created_at TEXT,
    updated_at TEXT
)
""")
conn.commit()

# ---------------------------
# Endpoints Portafolio
# ---------------------------
@app.get("/")
def read_root():
    return {"mensaje": "Hola, este es mi backend con FastAPI"}

@app.get("/proyectos")
def get_proyectos():
    return [
        {"nombre": "Focus", "url": "https://lucasmiguelsant.github.io/Focus/"}
    ]

# ---------------------------
# Endpoints Focus
# ---------------------------
@app.get("/health")
def health():
    """Endpoint para UptimeRobot, mantiene Render despierto."""
    return {"ok": True}

@app.get("/tareas")
def get_tareas():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    return [
        {
            "id": r[0],
            "title": r[1],
            "note": r[2],
            "datetime": r[3],
            "status": r[4],
            "created_at": r[5],
            "updated_at": r[6],
        }
        for r in rows
    ]

@app.post("/tareas")
def create_tarea(task: Task):
    task.id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    cursor.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (task.id, task.title, task.note, task.datetime.isoformat(), task.status, now, now))
    conn.commit()
    return {"ok": True, "task": task}

@app.put("/tareas/{task_id}/completar")
def completar_tarea(task_id: str):
    now = datetime.utcnow().isoformat()
    cursor.execute("UPDATE tasks SET status=?, updated_at=? WHERE id=?", ("done", now, task_id))
    conn.commit()
    return {"ok": True}
