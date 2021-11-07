from fastapi import FastAPI
from chat import getResponse

app = FastAPI()

@app.post('/')
def index(query: str):
    return getResponse(query)