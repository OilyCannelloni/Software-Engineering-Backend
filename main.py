import asyncio

from fastapi import FastAPI
from routers import default_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


origins = ["http://localhost:4200"]  # default URL for locally hosted Angular app

app = FastAPI()

# suppresing the warning related to type of the CORSMiddleware,
# because according to FastAPI devs this code is correct: https://github.com/tiangolo/fastapi/discussions/10968

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(default_router.router)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    # https://stackoverflow.com/questions/66275747/how-to-use-event-loop-created-by-uvicorn
    # trust me it works
    # noinspection PyTypeChecker
    config = uvicorn.Config(app=app, loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())
