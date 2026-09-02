# post request
'''
In FastAPI, a POST request is an HTTP method used to send data to the server to create or update a resource. 
FastAPI makes it easy to define endpoints that handle POST requests using Python decorators and type hints.
'''
from fastapi import FastAPI

from typing import Optional

app = FastAPI()




#to create a post request

@app.post('/blog')
def create_blog():
    
    return {'data': 'Blog is created'}





#anther example 
from pydantic import BaseModel

class Blog(BaseModel):       #block model
    
    title: str
    auther : str
    body: str
    published: Optional[bool]

@app.post('/blog_new')
def create_blog(blog: Blog): #used block model
    
    return {'data': f'Blog is created with title as {blog.title}'}



# post Request

@app.post('/student_v1')
def student(Name,semester):
    
    return {'Name': Name, 'semester': semester}

# post Request with pydantic class 
from pydantic import BaseModel

class Student(BaseModel):
    
    Name: str
    semester: int

@app.post('/student_v2')
def student(request: Student):  
    
    return request
