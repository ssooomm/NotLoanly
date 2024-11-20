from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from domain.dashboard import dashboard_router
from domain.notification import notification_router

app = FastAPI(debug=True)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router.router)
app.include_router(notification_router.router)