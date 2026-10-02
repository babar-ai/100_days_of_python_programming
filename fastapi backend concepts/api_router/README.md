# FastAPI APIRouter (Simple & Easy Guide)

## What is APIRouter?
Think of **`FastAPI()`** as your main website or app, and **`APIRouter()`** as different pages or sections.

Instead of writing all your code in one giant file, you use **`APIRouter`** to divide your app into groups (like Students, Courses, Bookings).

---

## Why do we use it?

1. **Avoid Repeating URLs (`prefix`)**:
   Instead of typing `/students/all`, `/students/add`, `/students/delete` every time, you set `prefix="/students"`. FastAPI automatically adds it in front of every URL.

2. **Organized Documentation (`tags`)**:
   In `http://127.0.0.1:8000/docs`, your endpoints will be neatly grouped under titles like **Students** and **Courses**.

3. **Clean Code**:
   Keeps your code simple, readable, and easy to maintain.

---

## How It Works in 4 Simple Steps

```python
from fastapi import FastAPI, APIRouter

# 1. Main app
app = FastAPI()

# 2. Create a router with prefix and tag
student_router = APIRouter(prefix="/students", tags=["Students"])

# 3. Add routes using the router
@student_router.get("/")
def get_students():
    return {"students": ["Ali", "Sara"]}

# 4. Attach the router to the main app
app.include_router(student_router)
```

---

## How to Run It:

Open your terminal in this folder and run:

```bash
uvicorn api_router:app --reload
```

Then open your browser at:
- **API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
