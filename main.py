from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users, products, auth

app = FastAPI(title="Codit API")

origins = [
 "http://localhost:4200",
 "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)

