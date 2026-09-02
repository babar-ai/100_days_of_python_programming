from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {"message": {"name" : "welocome to FastAPI"}}


@app.get('/about')
def about():
    return {'data':'about Data' }