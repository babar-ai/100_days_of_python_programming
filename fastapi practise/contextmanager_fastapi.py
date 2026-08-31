from contextlib import asynccontextmanager
from fastapi import FastAPI



@asynccontextmanager
async def lifespan(app: FastAPI):

    #STARTUP
    print("Application started")

    yield

    #SHUTDOWN
    print("Application shutting down")

app = FastAPI(lifespan=lifespan)


'''
Note: The important part is:

yield

Everything before yield runs during startup.

Everything after yield runs during shutdown.

Why is this useful?

Suppose you have a Redis connection pool:

redis_pool = None

You don't necessarily want to create and destroy it for every request.

Instead:

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Creating Redis pool")

    app.state.redis = create_redis_pool()

    yield

    print("Closing Redis pool")

    await app.state.redis.close()

Common examples:

Redis connection pools
Database connection pools
ThreadPoolExecutor
ML models
HTTP clients
LangGraph resources
caches
external service connections

'''