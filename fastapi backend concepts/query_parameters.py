from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get('/blog')                                                           #http://127.0.0.1:8000/blog?length=10&published=True
def index(length=10, published:bool=True, sort: Optional[str]= None, auther: Optional[str]= None):       #here 10 and true are default values
    
    if published:
        
        return {'data': f'{length} published blogs of the {auther} auther from db'}
    else:
        return {'data': 'all the unpublished blogs from db'}
    





#how to fastapi will know whether the 'id' is path parameter or query parameter
'''
remember: path parameter are always mention in route while query parameters are pass in url
'''
@app.get('/blog/{id}/comments')        #note : the varibale name 'id' should be same in both case i.e in path parameter and in path operation funtion
def comments(id, limit=10):
    
    return limit
    return {'data':{'1','2'}}
