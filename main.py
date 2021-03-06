import uvicorn
from fastapi import FastAPI

from api import urls

app = FastAPI(
    title='File server',
    description="""
    This api exposes file explorer enables to add, update, get and delete files.\n
    The root folder is "file_storage".""")

app.include_router(urls.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
