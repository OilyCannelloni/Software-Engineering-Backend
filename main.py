from fastapi import FastAPI
from routers import default_router

app = FastAPI()
app.include_router(default_router.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
