from fastapi import FastAPI, Depends

# FastAPI Depends (Dependency Injection System):
# - Used to share business logic, database sessions, and security/authentication.
# - Automatically resolves and injects dependencies into path operation functions.

app = FastAPI()


def get_user():
    return {"name": "Babar"}

@app.get("/profile")
def profile(user = Depends(get_user)):

    return user

