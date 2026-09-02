from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Session, select
from models import Hero, HeroCreate, HeroPublic, HeroUpdate
from Database import engine, create_db_and_tables



# Dependency to get a database session.. see readme
# This function provides a session to interact with the database.Used by FastAPI's Depends() to inject a live session into endpoints.
def get_session():                   
    with Session(engine) as session:
        yield session


# Annotated defines dependencies, validation
SessionDep = Annotated[Session, Depends(get_session)]                 
# Note: def read_items(db: SessionDep) == def read_items(db: Session = Depends(get_session))

app = FastAPI()


# We will create the database tables when the application starts.
# FastAPI event handler.It runs the function once when the application starts up — before it begins handling any requests.
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", status_code=200)  # RESPONSE STATUS CODE (See details in readme)
def home():
    return {"message": "Welcome to Hero API!"}


# Securely creating a new hero
@app.post("/heroes/", status_code=201)  # Hero_base -> name, age
def create_hero(hero: HeroCreate, session: SessionDep) -> HeroPublic:  
    # <- response_model Hero -> id, secret_name, HeroPublic -> id, HeroCreate -> secret_name

    # Convert Pydantic model (HeroCreate) to a SQLModel object (Hero)
    db_hero = Hero.model_validate(hero)

    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    
    return db_hero


# Read all heroes with pagination support
@app.get('/heroes', status_code=200)
def read_heroes(session: SessionDep, offset: int = 0, limit: int = 100):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


# Read a single hero
@app.get('/heroes/{hero_id}', status_code=200)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)  
    # get() is a method provided by SQLAlchemy and SQLModel to fetch a single record by its primary key.
    
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    return hero


# Update a Hero with HeroUpdate
@app.patch('/heroes/{hero_id}', response_model=HeroPublic, status_code=201) #instead of status_code=201
def update_hero(hero_id: int, session: SessionDep, hero: HeroUpdate):
    hero_db = session.get(Hero, hero_id)

    if not hero_db:                                            
        raise HTTPException(status_code=404)

    hero_data = hero.model_dump(exclude_unset=True)              # Extracts only the fields that the user actually sent in the request.
    hero_db.sqlmodel_update(hero_data)                           # Applies the changes to the hero instance.

    session.add(hero_db)                                         # Marks the hero object for an update.
    session.commit()                                             # Saves the changes in the database.
    session.refresh(hero_db)
    
    return hero_db


# Delete a hero
@app.delete('/hero/delete', status_code=200)
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)

    if not hero:  # Fixed condition (was checking `hero_id` instead of `hero`)
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()
    
    return {'ok': True}
