from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import jobs, stats, sync

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for all origins (less secure)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router)
app.include_router(stats.router)
app.include_router(sync.router)