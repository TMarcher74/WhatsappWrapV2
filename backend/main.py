"""
Project Title: Not decided

Routes:
    - Status : This route contains the status of the backend and other details like request header
    - Analyse : This route is responsible for accepting the chat data, send it to parser.py and return results
"""

from fastapi import FastAPI
from Routes import status, analyse, upload
import uvicorn

app = FastAPI()
app.include_router(status.router)
app.include_router(upload.router)
app.include_router(analyse.router)


# Backend start here, run main to run backend
if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
