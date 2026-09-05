import asyncio

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


async def generate_response():

    words = [
        "Hello",
        "I",
        "am",
        "streaming",
        "this",
        "response",
        "word",
        "by",
        "word."
    ]

    for word in words:

        yield word + ' '               # yield doesn't return everything at once.
        await asyncio.sleep(0.5)


@app.get("/stream")
async def stream():

    return StreamingResponse(
        generate_response(),
        media_type="text/plain")


