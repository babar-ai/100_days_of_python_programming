#uv pip install sse-starlette

import asyncio

from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse

app = FastAPI()


async def generate_events():

    words = ["Hello", "this", "is", "SSE", "streaming"]

    for word in words:
        yield {
            "data": word
        }

        await asyncio.sleep(0.5)


@app.get("/stream")
async def stream():

    return EventSourceResponse(generate_events())