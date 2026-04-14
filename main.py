from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users, products, auth

app = FastAPI(title="Codit API")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,  # Debe ser False cuando se usa "*" en origins
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)

