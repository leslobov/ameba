from fastapi import FastAPI

# Simple test app
app = FastAPI(title="Test API")


@app.get("/")
async def root():
    return {"message": "Test API is working"}


@app.get("/api/test")
async def test():
    return {"status": "OK"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
