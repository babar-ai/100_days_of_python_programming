from sqlmodel import SQLModel, Field        # SQLModel(ORM) = pydantic+sqlalchemy = Object relational mapping, 
                                            # Field: Used to add metadata (like primary keys, defaults, etc.) to model fields.

#SQLModel is a library built on top of SQLAlchemy and Pydantic.
    
class HeroBase(SQLModel):                  # Inherits from SQLModel to get Pydantic + SQLAlchemy features. True indicate to create table 
    
    name: str = Field(index = True)
    age: int | None = Field(default=None, index = True)      # index= True :  it means that an index will be created for the column in the database.
    
    
class Hero(HeroBase, table=True):         
    
    id: int | None = Field(default=None, primary_key=True)   #The ID can be an integer or None at initial stage when tabel is created        
    secret_name: str 
    

# HeroPublic - the public data model
# note: All the fields in HeroPublic are the same as in HeroBase, with id declared as int (not None):will be returned to the clients of the API.

class HeroPublic(HeroBase):                     
    
    id: int
    
# HeroCreate - the data model to create a hero

class HeroCreate(HeroBase):
    
    secret_name : str

#note: Now, when the clients create a new hero, they will send the secret_name, it will be stored in the database, but those secret names won't be returned in the API to the clients.
#tip: This is how you would handle passwords. Receive them, but don't return them in the API.

class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None