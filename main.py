from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from database import engine, Base
from exceptions import (
    CustomException,
    custom_exception_handler,
    validation_exception_handler,
    http_exception_handler
)
from routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API")

app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)