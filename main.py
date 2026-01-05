from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Permitir tu dominio de GitHub Pages
origins = [
    "https://lucasmiguelsant.github.io",  # tu portafolio
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # o ["*"] si quieres permitir todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Portafolio
# ---------------------------
@app.get("/")
def read_root():
    return {"mensaje": "Hola, este es mi backend con FastAPI"}

@app.get("/proyectos")
def get_proyectos():
    return [
        {"nombre": "Portafolio", "url": "https://lucasmiguelsant.github.io/portafolio/"},
        {"nombre": "Otro proyecto", "url": "https://ejemplo.com"}
    ]

# ---------------------------
# Focus (tareas y alarmas)
# ---------------------------

# Modelo de tarea
class Task(BaseModel):
    id: str
    title: str
    note: str | None = None
    datetime: datetime
    status: str = "pending"

# Memoria temporal (luego puedes usar DB)
TASKS = []

@app.get("/health")
def health():
    """Endpoint para UptimeRobot, mantiene Render despierto."""
    return {"ok": True}

@app.get("/tareas")
def get_tareas():
    return TASKS

@app.post("/tareas")
def create_tarea(task: Task):
    TASKS.append(task.dict())
    return {"ok": True, "task": task}

@app.put("/tareas/{task_id}/completar")
def completar_tarea(task_id: str):
    for t in TASKS:
        if t["id"] == task_id:
            t["status"] = "done"
            return {"ok": True, "task": t}
    return {"error": "Tarea no encontrada"}
