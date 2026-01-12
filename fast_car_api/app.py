from fastapi import FastAPI
from routes import router as car_router
from database import Base, engine
import models  # IMPORTANTE: força o registro dos models

import os

app = FastAPI(title="Fast Car Api")

# 👇 Mostra exatamente ONDE o SQLite está criando o arquivo
print("USANDO BANCO EM:", os.path.abspath("cars.db"))

# 👇 Cria as tabelas se não existirem
Base.metadata.create_all(bind=engine)

# 👇 Registra as rotas
app.include_router(car_router)

@app.get("/")
def read_root():
    return {"status": "ok"}
