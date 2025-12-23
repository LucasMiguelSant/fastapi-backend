from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def read_root():
    return {"mensaje": "Hola, este es mi backend con FastAPI"}

@app.get("/proyectos")
def get_proyectos():
    return [
        {"nombre": "Portafolio", "url": "https://lucasmiguelsant.github.io/portafolio/"},
    ]

