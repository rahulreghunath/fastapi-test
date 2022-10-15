from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List
from blog.messages import BLOG_ADDED
from blog.response_schemas import RESPONSE_404, RESPONSE_OK
from . import schemas, models
from .database import engine, get_db

app = FastAPI()
models.Base.metadata.create_all(engine)


@app.post(
    '/blog',
    status_code=status.HTTP_201_CREATED,
    responses={
         status.HTTP_201_CREATED: RESPONSE_OK,
    }
)
def new_blog(request: schemas.BlogCreate, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'details': BLOG_ADDED}


@app.get(
    '/blog',
    responses={
         status.HTTP_200_OK: {
            "model": List[schemas.Blog],
            "description":"List of Blogs"
        },
    }
)
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get(
    '/blog/{id}',
    responses={
        status.HTTP_200_OK: {"model": schemas.Blog},
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
    },
)
def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).get(id)
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
    return blog

@app.delete(
    '/blog/{id}',
    responses={
        status.HTTP_200_OK: RESPONSE_OK,
        status.HTTP_404_NOT_FOUND: RESPONSE_404        
    },
    status_code=status.HTTP_200_OK
)
def delete_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Blog not found')
    blog.delete(synchronize_session=False)
    
    db.commit()
    
    return {'details':'Blog deleted'}    

@app.put(
    '/blog/{id}',
    responses={
        status.HTTP_202_ACCEPTED: RESPONSE_OK,
        status.HTTP_404_NOT_FOUND: RESPONSE_404        
    },
    status_code=status.HTTP_202_ACCEPTED
)
def update_blog(
    id: int,
    request:schemas.Blog,     
    db: Session = Depends(get_db)
):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Blog not found')
    blog.update(request.dict(),synchronize_session=False)    
        
    db.commit()
    
    return {'details':'Blog updated'}  

@app.patch(
    '/blog/{id}',
    responses={
        status.HTTP_202_ACCEPTED: RESPONSE_OK,
        status.HTTP_404_NOT_FOUND: RESPONSE_404        
    },
    status_code=status.HTTP_202_ACCEPTED
)
def partial_update_blog(
    id: int,
    request:schemas.BlogUpdate,     
    db: Session = Depends(get_db)
):
    updated_request=request.dict(exclude_unset=True)
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Blog not found')
    blog.update(updated_request)
    db.commit()
    
    
    return {'details':f'Blog updated'}    
