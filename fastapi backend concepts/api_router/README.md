# FastAPI APIRouter: Comprehensive Guide & Practical Use Cases

## 1. What is `APIRouter`?

In **FastAPI**, `APIRouter` is a class used to group related endpoints (routes) into smaller, reusable, and modular sub-applications. 

Instead of attaching every single route to the main `app = FastAPI()` object, you define routes on an `APIRouter` instance and then **mount/include** them into your main application using `app.include_router(...)`.

---

## 2. Why Do We Use `APIRouter`?

### A. Separation of Concerns & Clean Code
Without `APIRouter`, a real-world backend with dozens of endpoints (authentication, users, payments, orders, notifications) would force everything into a massive, cluttered `main.py` file. `APIRouter` keeps each domain logic cleanly separated in its own file or module.

### B. Common URL Prefixes
Avoid repeating base path strings across dozens of endpoints:
```python
# Instead of writing /users/profile, /users/settings, /users/list:
router = APIRouter(prefix="/users")

@router.get("/list")      # Resolves to: /users/list
@router.get("/profile")   # Resolves to: /users/profile
```

### C. Swagger / OpenAPI Documentation Grouping
With the `tags` argument, endpoints are grouped into neat sections in the `/docs` UI:
```python
router = APIRouter(prefix="/products", tags=["Products"])
```

### D. Shared Dependencies (Auth, Permissions, Rate Limits)
You can apply authentication or validation rules across **all** endpoints inside a router at once:
```python
router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(verify_admin_token)]
)
```

### E. Team Collaboration
Allows multiple developers to work independently on separate features (e.g., developer A on `users.py`, developer B on `orders.py`) without merge conflicts in `main.py`.

---

## 3. Recommended Production Project Structure

In real-world applications, `APIRouter` is structured as follows:

```text
my_project/
│
├── main.py                     # Initializes FastAPI and includes routers
├── core/
│   ├── config.py               # Settings and environment variables
│   └── database.py             # DB connection session
│
├── routers/                    # Dedicated folder for all routers
│   ├── __init__.py
│   ├── auth.py                 # router for /auth (login, register, token refresh)
│   ├── users.py                # router for /users (profiles, update user)
│   ├── products.py             # router for /products (catalog, inventory)
│   └── orders.py               # router for /orders (cart, checkout)
│
└── schemas/                    # Pydantic models for validation
    ├── user.py
    └── product.py
```

---

## 4. Key Parameters of `APIRouter`

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| `prefix` | `str` | Prepend a base path (e.g., `prefix="/api/v1/users"`) |
| `tags` | `List[str]` | Groups routes in Swagger UI (`/docs`) and ReDoc |
| `dependencies` | `List[Depends]` | Enforce dependencies (auth, permissions) on every route in this router |
| `responses` | `Dict` | Define shared HTTP responses (e.g., custom 404, 401 schemas) |
| `include_in_schema` | `bool` | Set to `False` to hide all endpoints in this router from public docs |

---

## 5. Nesting Routers (Advanced Feature)

You can also include an `APIRouter` inside another `APIRouter`. This is helpful for nested resources like `/users/{user_id}/orders`:

```python
from fastapi import APIRouter

user_router = APIRouter(prefix="/users")
orders_router = APIRouter(prefix="/{user_id}/orders")

@orders_router.get("/")
def get_user_orders(user_id: int):
    return {"user_id": user_id, "orders": []}

# Nest orders under users:
user_router.include_router(orders_router)

# Final path becomes: /users/{user_id}/orders/
```

---

## 6. How to Run the Practical Example

The practical example is provided in [`api_router.py`](file:///d:/All%20other%20stuffs/100_days_of_Python_course/fastapi%20backend%20concepts/api_router/api_router.py).

### Step 1: Open Terminal in this folder
```bash
cd "d:\All other stuffs\100_days_of_Python_course\fastapi backend concepts\api_router"
```

### Step 2: Run with Uvicorn
```bash
uvicorn api_router:app --reload
```
or run python directly:
```bash
python api_router.py
```

### Step 3: Test Interactive API Docs
Open your browser and navigate to:
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Alternative**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Notice how the endpoints are grouped under **Users**, **Products**, and **Root** sections.
