#post request

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

#pydantic is a data validation and settings management library for Python, which uses Python type annotations.
# It provides a way to define data models and validate data against those models, making it easier to work with structured data in Python applications.

#lets create a data model for student info
#A Pydantic model used to validate the data in the request body
#User Authentication: Sending login credentials to a server to authenticate a user.
class Student(BaseModel):
    Name: str
    semester: int
    age: int
    gender: Optional[str] = None  # Optional field, default is None


app = FastAPI()

@app.post('/studentinfo')
def student_info(student: Student):
    return {"message": "Student information received", "data": student.dict()}