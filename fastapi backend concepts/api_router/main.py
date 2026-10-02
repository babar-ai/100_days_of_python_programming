from fastapi import FastAPI, APIRouter
from routers.students import student_router
from routers.course import course_router


# Step 1: Create the main FastAPI app
app = FastAPI()

# Main homepage route
@app.get("/")
def home():
    # URL: http://127.0.0.1:8000/
    return {"message": "Welcome to School API! Go to /docs to test."}


# Step 4: Plug the routers into the main app
app.include_router(student_router)
app.include_router(course_router)