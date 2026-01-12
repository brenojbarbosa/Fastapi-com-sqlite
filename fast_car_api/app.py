from fastapi import FastAPI
from routes import router as car_router
from database import Base, engine
import models

import os

app = FastAPI(title="Fast Car Api")


print("USANDO BANCO EM:", os.path.abspath("cars.db"))


Base.metadata.create_all(bind=engine)


app.include_router(car_router)

@app.get("/")
def read_root():
    return {"status": "ok"}
