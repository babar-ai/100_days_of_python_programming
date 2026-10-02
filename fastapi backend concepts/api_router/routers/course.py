from fastapi import FastAPI, APIRouter



# Step 3: Create another Router for "Courses"
# Any route here will automatically start with "/courses"
course_router = APIRouter(prefix="/courses", tags=["Courses"])

@course_router.get("/")
def get_all_courses():
    # URL: http://127.0.0.1:8000/courses/
    return {"courses": ["Python", "FastAPI", "Data Science"]}