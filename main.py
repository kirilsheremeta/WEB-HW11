from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.db import get_db
from src.routes import contacts

app = FastAPI()
app.include_router(contacts.router, prefix='/api')


@app.get('/')
async def root():
    return {'message': 'Welcome!'}


@app.get('/api/healthchecker')
def healthchecker(db: Session = Depends(get_db)):
    try:
        request = db.execute(text('SELECT 1')).fetchone()
        if request is None:
            raise HTTPException(status_code=500, detail='Database is not configured correctly')
        return {'message': 'Welcome to FastAPI'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Error connecting to the database')
