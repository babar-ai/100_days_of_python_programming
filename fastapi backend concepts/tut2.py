from fastapi import FastAPI

app = FastAPI()

@app.get('/')                              #operation: is get.. '/' is the path where '@' is 'path operation decorator'
def index():
    return {"message": {"name" : "welocome to FastAPI"}}

                                          #A "path" is also commonly called an "endpoint" or a "route".
@app.get('/about')                        # here 'get' is the operation on the path and ('/') is the path where '@app' is 'path operation decorator'
def aboutme():                            #this is path operation funtion where fun name does't matter
    return {'data':'welcome to learning fastapi' }         


@app.get('/product')
def get_product():
    return {'items': ['watch', 'phone', 'laptop'], 'message': 'welcome to fastapi'}