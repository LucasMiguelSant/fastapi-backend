from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
@app.get("/proyectos")
def get_proyectos():
    return [
        {"nombre": "Focus", "url": "https://lucasmiguelsant.github.io/Focus/"}
    ]
