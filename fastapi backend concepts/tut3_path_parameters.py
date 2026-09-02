from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data': 'blog list'}

@app.get('/blog/unpublished')                  # if we have a rout like this we must have to keep it above the dynamic route because it will generate error i.e it fastapi will aspect the same datatype value
def unpublished():                             # now it's at fine location 
    return {'data': 'all unpublished blogs'}

@app.get('/blog/{id}')                       # '{id}' indicate dynamic path parameters and overall path is known by dynamic routing
def show(id:int):                            # as we define integer datatype here so if we provide an string as path parameter fastapi will show error meassage
    
    #fetch blog with id = id                    
    return {'data': id  }


@app.get('/blog/unpublished')                  # if we have a rout like this we must have to keep it above the dynamic route because it will generate error i.e it fastapi will aspect the same datatype value
def unpublished():
    return {'data': 'all unpublished blogs'}



@app.get('/blog/{id}/comments')        #note : the varibale name 'id' should be same in both case i.e in path parameter and in path operation funtion
def comments(id):
    
    return {'data':{'1','2'}}

# Advanced Example with Multiple Path Parameters

@app.get('/user/{user_id}/product/{product_id}')
def get_user_product(user_id: int, product_id: int) -> dict:
    return{'data': f'User {user_id} has product {product_id}'}