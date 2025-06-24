from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.middleware.user_manager import AttachUserIDMiddleware
from api.routes import users, admin, interview
from api.database import init_indexes

app = FastAPI()

# CORS setup (for frontend dev)
origins = ["http://localhost:3000"]


# Reigster Middlewars
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AttachUserIDMiddleware)


# Register routes
app.include_router(users.router, prefix="/auth", tags=["users"])
app.include_router(interview.router, prefix="/interview", tags=["interview"])




# Startup logic for MongoDB (optional: e.g. create indexes)
@app.on_event("startup")
async def startup_event():
    await init_indexes()
