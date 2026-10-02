from fastapi import FastAPI, APIRouter


# Step 2: Create a Router for "Students"
# Any route here will automatically start with "/students"
student_router = APIRouter(prefix="/students", tags=["Students"])

@student_router.get("/")
def get_all_students():
    # URL: http://127.0.0.1:8000/students/
    return {"students": ["Ali", "Sara", "Ahmed"]}

@student_router.get("/{student_id}")
def get_single_student(student_id: int):
    # URL: http://127.0.0.1:8000/students/1
    return {"student_id": student_id, "name": "Ali"}