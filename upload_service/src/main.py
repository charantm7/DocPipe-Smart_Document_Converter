from fastapi import FastAPI

app = FastAPI()


@app.get("/upload/file")
def upload():
    return {"message": "hi this is upload router"}
