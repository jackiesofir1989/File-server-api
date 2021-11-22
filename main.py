import uvicorn
from fastapi import FastAPI

from api import urls

app = FastAPI(title='File Server')

app.include_router(urls.router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level="info", reload=True)
