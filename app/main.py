from fastapi import FastAPI

from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker

from crud import get_news_info,get_db_url
from models import Base

app = FastAPI()

@app.get('/Hello_world')
async def Hello():
    return {'Hello World!'}


@app.post('/database/create_table',tags = ['Database'])
async def Create_Table():
    try:
        DATABASE_URL,database = get_db_url()

        engine = create_engine(DATABASE_URL,echo = True)

        with engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))

        engine_url = engine.url.set(database = database)
        with create_engine(engine_url).connect() as connection:
            result = Base.metadata.create_all(bind = connection, checkfirst = True)

        return {
            'result':True,
            'msg':'Create table success'
        }
    except Exception as e:
        return{
            'result':False,
            'msg':f'{str(e)}'
        }
