from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.router import api_router


app = FastAPI(
    title="School Management Platform API",
    description="Backend API for the School Listing and Management Platform",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the School Management Platform API",
        "status": "running"
    }