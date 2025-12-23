from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "Hola, este es mi backend con FastAPI"}

@app.get("/proyectos")
def get_proyectos():
    return [
        {"nombre": "Portafolio", "url": "https://lucasmiguelsant.github.io/portafolio/"},
        {"nombre": "Otro proyecto", "url": "https://..."}
    ]
