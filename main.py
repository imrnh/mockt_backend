from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import users, admin, interview
from api.database import init_indexes

app = FastAPI()

# CORS setup (for frontend dev)
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(users.router, prefix="/auth", tags=["users"])
app.include_router(interview.router, prefix="/interview", tags=["interview"])

# app.include_router(admin.router, prefix="/admin", tags=["admin"])

# Startup logic for MongoDB (optional: e.g. create indexes)
@app.on_event("startup")
async def startup_event():
    await init_indexes()
