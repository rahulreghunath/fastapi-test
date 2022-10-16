from typing import Union
from pydantic import BaseModel


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }
        
class HTTPSuccess(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Response message"},
        }

class Blog(BaseModel):
    title: Union[str,None] = None
    body: Union[str,None] = None
    
class ShowBlog(Blog):
    class Config:
        orm_mode = True
    
class BlogCreate(Blog):
    title: str
    body: str
    
class BlogUpdate(BaseModel):
    title: Union[str,None] = None
    body: Union[str,None] = None

class User(BaseModel):
    name: str
    email: str
    password : str