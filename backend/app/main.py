from fastapi import FastAPI


app = FastAPI(title="Voyagent Backend API")

@app.get("/")
def read_root():
    return {"Hello": "World"}