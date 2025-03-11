from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from crud import get_news_info,get_db_url
from models import Base,News
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


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

@app.post('/grep_news',tags = ['WebCrawler'])
async def GrepNews():
    try:
        DATABASE_URL,database = get_db_url()

        engine = create_engine(DATABASE_URL+f'/{database}')

        Session = sessionmaker(bind = engine)
        session = Session()

        news = get_news_info()

        for item in news:
            existing_news = session.query(News).filter(News.title == item['title']).first()
            if not existing_news:
                data = News(
                    title = item['title'],
                    url = item['link']
                )
                session.merge(data)
                session.commit()
        session.close()
        return {
            'result':True,
            'msg' : 'Get News success'
        }
    except Exception as e:
        return{
            'result':False,
            'msg':f'{str(e)}'
        }



@app.get('/database/get_news_list',tags = ['Database'])
async def Get_News_List():
    try:
        DATABASE_URL,database = get_db_url()

        engine = create_engine(DATABASE_URL+f'/{database}',echo = True)
        Session = sessionmaker(bind = engine)
        session = Session()
        news = session.query(News).all()
        return {
            'result':True,
            'msg':'Create table success',
            'object':news
        }
    except Exception as e:
        return{
            'result':False,
            'msg':f'{str(e)}',
            'object':[]
        }
