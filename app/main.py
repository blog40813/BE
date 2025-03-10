from fastapi import FastAPI

app = FastAPI()

@app.get('/Hello_world')
async def Hello():
    return {'Hello World!'}