from fastapi import FastAPI

app = FastAPI()


@app.get('/')      # ('/) --> path,  .get('/') --> operation on the path,      @app -->path opeation decorator
def index():       # this fun is call "path operation funtion"               note: the funtion name does't effect the server running it cant be changable
    return 'hey'


# as mostly we will deal data in json file format lets return data in json format
@app.get('/new')
def index1():
    return {'data': {'name': "Babar"}}

#let create about page  

@app.get('/about/{id}')        # --> about path : it is  all dynamic routing
def about(id: int):
    return {'about':'This is about page welcome to fastapi','data': id}
 
 
 
#we can use swagger app for testing your api without having Ui
# to access swagger just type doc "http://localhost:8000/docs#" like this


#Query Parameteres
'''

In FastAPI, query parameters are a way to send additional data to your API endpoints in the URL's query string. Query parameters are typically used to filter,
sort, or customize the response of a request.

Query parameters are included in the URL after a ? and are specified as key-value pairs, separated by &. For example:
/item?skip=10&limit=15
'''

@app.get('/items')
def read_item(skip: int = 0, limit: int = 10): #here 'skip' and 'limit' is the query parameters
    
    return {"skip": skip, "limit": limit}



#Request Body
'''
# Request Body
A request body is data sent by the client (e.g., browser, mobile app) to the server in an HTTP request.
The request body typically contains structured data that the server needs to process the request, such as user input, form data, or JSON objects.
example :  registration form
'''
#post request
'''


'''
from pydantic import BaseModel        
from typing import Optional

class Student(BaseModel):
     
    name: str                           # Attendtion : By default, Pydantic treats all fields as required
    age: int
    graduated: Optional[str] = None


@app.post('/studentinfo')
def student_Info(student: Student):
    return {'data': f"The Name of the Student is {student.name}. Cool!"}
    
    
    
    
    
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from fastapi import FastAPI

app = FastAPI()

@app.get('/')                             # The @app.get('/') decorator maps the root URL (/) to the index function.

def index():
    return {'data':{'name':'Babar'},      # The function returns a Python dictionary that FastAPI automatically converts into a JSON response.
            'is_student': True
            
            }

@app.get('/about')  #path
def about():
    return {'about page': {"this is my first page"}}

@app.get('/blog/{id}')
def show(id: int):
    
    return {'data': id}  

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++