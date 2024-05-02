import os
import pickle

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from app.routes.routes import router
from app.utils import start_ngrok
from app.utils.create_context import load_data_to_db


app = FastAPI()
app.include_router(router)

# start_ngrok()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    if not os.path.exists("database") or os.listdir("database") == []:
        data_info = pickle.load(open("data.pkl", "rb"))
        load_data_to_db(data_info)

    uvicorn.run(app, host="localhost", port=8001, workers=1)