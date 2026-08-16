from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.mongodb import client
from app.routers import auth, products


@asynccontextmanager #It tells Python that this function is an asynchronous context manager.
#this allows you to define: Before yield → startup | After yield  → shutdown
async def lifespan(app: FastAPI):
    await client.admin.command("ping") #checks that MongoDB is reachable.

    print("MongoDB connected successfully")

    yield #At this point, FastAPI starts accepting requests.
    #Startup is finished. Let the application run.
    # When the application shuts down, continue from here.

    await client.close() #When FastAPI shuts down:

    print("MongoDB connection closed")


app = FastAPI(
    title="FastAPI MongoDB CRUD API",
    description=(
        "CRUD API with MongoDB, "
        "JWT authentication, "
        "Pydantic validation, "
        "and service layer architecture."
    ),
    version="1.0.0",
    lifespan=lifespan
)

#register the routers
app.include_router(auth.router) 
app.include_router(products.router)


@app.get("/")
async def root():
    return {
        "message": "FastAPI MongoDB API is running"
    }


@app.get("/health")
async def health():
    await client.admin.command("ping")

    return {
        "status": "ok",
        "database": "connected"
    }