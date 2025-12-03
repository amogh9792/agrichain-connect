---

📅 Date: 27-11-2025

🎫 Tickets Worked On:

- BE-001 – Project Initialization & Environment Setup

📝 Today's Tasks:

- Created GitHub repo
- Added initial folder structure for app/
- Created requirements.txt and README
- Added docker-compose.yml
- Created .env file for DB credentials
- Started PostgreSQL container successfully

💻 Commands Used:
docker compose up -d
docker compose ps

📂 Files Modified:

- docker-compose.yml
- .gitignore
- README.md

🐞 Issues Faced:

- Docker Desktop engine was not running → got pipe error
- Clarified how ${VAR} works in docker compose

🛠 How Issues Were Solved:

- Restarted Docker Desktop
- Enabled WSL
- Added correct DB_HOST in .env

📚 Learnings:

- Docker Compose reads .env automatically
- Using .env avoids exposing DB credentials
- Project skeleton must be created before backend logic
- Docker must be running before using docker compose.
- Docker Compose automatically reads .env for variable replacement.
- Using .env prevents exposing credentials inside docker-compose.yml.
- Postgres container now runs isolated from system environment.
- Project skeleton must be completed before any backend coding.

➡️ Next Steps:

- Implement connection.py
- Setup Alembic and migrations

---

---

# 📅 Date: 27-11-2025

# 🎫 Tickets Worked On:

- **BE-002 – Database Setup, Environment Fixes & Alembic Initialization**

---

# 📝 Today's Tasks:

- Added `docker-compose.yml` to run PostgreSQL using Docker
- Created `.env` file for storing DB username & password securely
- Installed and configured **SQLAlchemy** (ORM)
- Installed and configured **Alembic** for database migrations
- Fixed Windows PostgreSQL service conflict
- Ensured Docker PostgreSQL is the only active database
- Successfully created & applied initial Alembic migration

---

### 🐘 What is PostgreSQL?

A relational SQL database that stores all backend data: users, farmers, vendors, inventory, orders, etc.

### 🐳 What is Docker & Why Did We Use It?

Docker creates a **mini isolated environment** where PostgreSQL runs safely without interfering with Windows.  
No installation headaches, no version conflicts, same environment for all developers.

### 🧠 What is SQLAlchemy?

A Python ORM (Object Relational Mapper).  
Lets us write **Python classes** instead of **raw SQL queries**.

### 🔧 What is Alembic & Why Use It?

Alembic is **Git for your database schema**.

- When models change → Alembic creates migration files
- Migration files keep database structure consistent everywhere
- Teams avoid schema conflicts
- Production DBs stay synchronized safely

Without Alembic, databases become mismatched and break the application.

---

# 💻 Commands Used:

### ▶ Start PostgreSQL using Docker

```sh
docker compose up -d
```

### ▶ Check running containers

```sh
docker compose ps
```

### ▶ Stop and reset database volume

```sh
docker compose down -v
```

### ▶ Enter PostgreSQL inside container

```sh
docker exec -it agrichain_db psql -U postgres
```

### ▶ Create database

```sql
CREATE DATABASE agrichain;
```

### ▶ Initialize Alembic

```sh
alembic init alembic
```

### ▶ Create migration file

```sh
alembic revision --autogenerate -m "initial migration"
```

### ▶ Apply migration

```sh
alembic upgrade head
```

---

# 📂 Files Modified:

- **docker-compose.yml**
- **.env**
- **alembic.ini**
- **alembic/env.py**
- **.gitignore**
- Initial migration in `alembic/versions/`

---

# 🐞 Issues Faced:

### ❌ Issue 1 – Alembic “database does not exist”

**Cause:**  
Windows had its own PostgreSQL service running on port 5432.  
Alembic connected to that instead of Docker PostgreSQL.

### ❌ Issue 2 – Another process using port 5432 (`wslrelay.exe`)

WSL networking was listening on IPv6 but did not break Docker.  
Needed verification to ensure Docker was still the primary.

### ❌ Issue 3 – Alembic could not autogenerate

`env.py` was missing correct project path + metadata import.

---

# 🛠 How Issues Were Solved:

- Stopped Windows PostgreSQL service

```sh
net stop postgresql-x64-17
```

- Restarted Docker containers
- Recreated database volume
- Updated `env.py` to load Base.metadata correctly
- Re-ran Alembic commands after fixing DB connection
- Verified successful migration creation & application

---

# 📚 Learnings:

- Only **one** process can use port 5432.
- Docker PostgreSQL is safer and isolated from OS conflicts.
- `.env` keeps passwords hidden and secure.
- Alembic is essential for keeping DB changes in sync.
- SQLAlchemy + Alembic is industry-standard for Python projects.
- Docker volumes store data persistently even after container restarts.
- Migrations prevent “works on my PC” database issues.

---

# ➡️ Next Steps:

- Start **BE-003 – Application Bootstrap**
  - Create `main.py`
  - Add `/health` route
  - Setup router structure
  - Connect DB session with FastAPI

---

---

📅 Date: 28-11-2025  
🎫 Ticket: BE-003 – FastAPI Application Bootstrap

---

🎯 **Objective**  
Set up the base FastAPI application with a clean folder structure, a configuration module, and a health-check API.  
This forms the foundation for all future modules (Auth, Farmer, Vendor, Orders, Produce).

📝 **Today's Tasks**

🌱 **1. Removed unused folder**

- Deleted old folder `app/routers/`  
  (We use `app/api/routes/` for the modern routing structure.)

⚙️ **2. Added configuration module**  
Created file: `app/core/config.py`  
Purpose:

- Loads `.env` variables
- Centralized project settings (DB, project name)
- Used later in DB connection, JWT config, email config, etc.

📁 **3. Created API routing structure**  
Created:

```
app/api/routes/
```

Purpose:  
This folder will store all API endpoints like `health.py`, `auth.py`, `farmer.py`, `vendor.py`, etc.

❤️ **4. Added Health Route**  
File: `app/api/routes/health.py`

Endpoint added:

```
GET /api/health
```

Expected response:

```json
{ "status": "ok", "version": "1.0" }
```

🚀 **5. Added main FastAPI entrypoint**  
File: `app/main.py`  
Purpose:

- Create FastAPI app
- Include routers
- Define global configuration (title, middleware coming later)

💻 **Commands Used**

```
mkdir app\core
mkdir app\api
mkdir app\api\routes
rmdir /s /q app\routers
uvicorn app.main:app --reload
```

Test API:  
`http://127.0.0.1:8000/api/health`

📂 **Files Modified / Added**

```
app/core/config.py
app/api/routes/health.py
app/main.py
app/api/routes/__init__.py
app/api/__init__.py
```

🐞 **Issues Faced**

❌ **ImportError: No module named app.api.routes.health**  
Cause:

- Missing folders or missing `__init__.py`.

Fix:

- Added correct structure and re-imported.

❌ **Confusion: “Where is health_router function?”**  
Clarification:

- `router = APIRouter()` is imported as:  
  `from health import router as health_router`
- It's an alias, not a function.

📚 **Learnings**

- FastAPI uses `APIRouter()` for modular design.
- `include_router()` mounts routes under a prefix.
- `config.py` centralizes environment variables.
- A clean project layout prevents future complexity.
- Aliasing imports (`router as health_router`) is common practice.
- `main.py` is always the entrypoint for FastAPI.

➡️ **Next Steps**

- Start BE-004 (User Model + Migration)
- Create SQLAlchemy models
- Create Alembic migration for `users` table
- Prepare `schemas` and `services` folder for upcoming Auth module

---

---

📅 Date: 29-11-2025

🎫 Ticket Worked On:

- **BE-004 – User Model & Database Migration**

📝 Today's Tasks:

- Created the first database entity: **User**
- Added SQLAlchemy model file under `app/models/`
- Linked Alembic to SQLAlchemy `Base.metadata`
- Generated migration using Alembic autogenerate
- Applied migration to PostgreSQL inside Docker container
- Verified that `users` table appears in DB

📂 Files Added/Modified:

- `app/models/user.py`
- `app/database/connection.py` (ensured Base is exported)
- `alembic/env.py` (configured target_metadata)
- `alembic/versions/xxxxxxxx_add_users_table.py` (auto migration)

💻 Commands Used:

- `alembic revision --autogenerate -m "add users table"`  
  Creates migration file based on model changes.
- `alembic upgrade head`  
  Applies the migration to the actual database.
- `docker exec -it agrichain_db psql -U postgres -c "\dt"`  
  Shows all tables inside the container DB.

🐞 Issues Faced:

- Alembic failing with:
  _“database agrichain does not exist”_
- Hostname `db` not resolving inside Alembic
- Local PostgreSQL Windows service occupying port 5432
- Docker PostgreSQL not getting correct port due to conflict

🛠 How Issues Were Solved:

- Stopped Windows PostgreSQL service (`postgresql-x64-*`)
- Restarted Docker Desktop after freeing port 5432
- Updated Alembic URL to:
  `postgresql://postgres:amogh@localhost:5432/agrichain`
- Ensured database exists by checking with:
  `docker exec -it agrichain_db psql -U postgres -c "\l"`
- Ran revision again after fixing metadata imports

📚 Learnings:

- Alembic needs SQLAlchemy `Base.metadata` to autogenerate tables.
- Local system PostgreSQL can conflict with Docker’s PostgreSQL.
- Docker container hostname (`db`) resolves only inside other containers, **not on Windows host**.
- Best practice: use `localhost` for Alembic when running locally.
- First table migration confirms DB setup, metadata wiring, and pipeline all work correctly.

➡️ Next Steps:

- Create User Pydantic schema
- Build User service layer (create + get user)
- Add `/users` API router
- Prepare BE-005 User Registration API

---

📅 Date: 30-11-2025

🎫 Ticket Worked On:

- BE-005 – User Registration API (Models → Schemas → Service → Router → Testing)

📝 Today's Tasks:

- Added Pydantic schemas for user creation & response
- Implemented password hashing using passlib + bcrypt
- Created UserService for business logic
- Added database session dependency using Depends()
- Implemented POST /users/register endpoint
- Validated duplicate emails
- Wired routes inside main.py
- Tested API on Swagger UI
- Fixed bcrypt installation issue
- Fixed Pydantic schema errors (missing type annotations)
- Ensured DB connection uses correct host (localhost not db)

📂 Files Added/Modified:

- app/schemas/user.py
- app/services/user_service.py
- app/api/routes/user_router.py
- app/database/session.py
- app/main.py

💻 Commands Used:

# Run server

uvicorn app.main:app --reload

# Install required packages

pip install passlib[bcrypt]
pip install email-validator

# Check if table exists in DB

docker exec -it agrichain_db psql -U postgres -c "\dt"

# Test API in Swagger

http://127.0.0.1:8000/docs

# Git workflow

git checkout -b BE-005-user-registration
git add .
git commit -m "BE-005: Implemented User Registration API"
git checkout main
git merge BE-005-user-registration
git push origin main

🐞 Issues Faced:

❌ Issue 1 – Pydantic error:
“created_at has no type annotation”
Reason: Pydantic v2 needs types for all fields.

Fix:
created_at: datetime

❌ Issue 2 – bcrypt backend error:
"module 'bcrypt' has no attribute '**about**'"

Fix:
pip uninstall bcrypt
pip install bcrypt==4.0.1

❌ Issue 3 – Hostname "db" not resolving
Reason: Alembic & FastAPI run on Windows host, not inside Docker.

Fix:
Use:
DB_HOST=localhost

❌ Issue 4 – Password longer than 72 bytes
Reason:
bcrypt has a 72-byte limit.

Fix:
Told user to use shorter password or trim input in frontend.

🛠 How Issues Were Solved:

- Updated DB_HOST to localhost everywhere outside Docker
- Cleaned up schemas to match Pydantic v2 rules
- Installed compatible bcrypt version
- Added proper session dependency for FastAPI
- Wrapped duplicate email error in HTTPException
- Restarted Docker container after DB fixes
- Verified migration exists and table is visible in PostgreSQL

📚 Learnings:

- Pydantic v2 is strict about field type annotations
- bcrypt enforces a maximum password length (72 bytes)
- Alembic uses localhost, not Docker-hostname, when executed on Windows
- Service layer keeps business logic clean and reusable
- Using Depends(SessionLocal) keeps DB session lifecycle correct
- FastAPI's automatic request parsing + validation reduces boilerplate
- Proper folder structure (models, schemas, services, routes) scales better

➡️ Next Steps:

- Start BE-006 – Login & JWT Authentication
- Add token generation service
- Add password verification logic
- Add protected routes (farmer/vendor/admin dashboards)





📅 Date: 30-11-2025
🎫 Ticket: BE-006 – User Authentication (Login + JWT Token Generation)

📝 Tasks Completed:
- Added JWT env variables: JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
- Installed packages: python-jose[cryptography], passlib[bcrypt], pydantic-settings
- Updated config.py to include JWT fields
- Created core/security.py → hashing + token creation
- Created services/auth_service.py → login logic
- Added POST /auth/login route in auth_router.py
- Updated main.py to include auth routes

📂 Files Modified/Added:
.env
app/core/config.py
app/core/security.py
app/services/auth_service.py
app/api/routes/auth_router.py
app/main.py

💻 Commands Used:
pip install python-jose[cryptography] passlib[bcrypt] pydantic-settings
uvicorn app.main:app --reload

🐞 Issues & Fixes:
1) BaseSettings import error → installed `pydantic-settings`
2) “Extra inputs not permitted” → added JWT fields to Settings model
3) uvicorn error “main not found” → correct command: uvicorn app.main:app --reload

📚 Learnings:
- JWT tokens need secret key + algorithm + expiry to work
- Pydantic v2 environment management comes from pydantic-settings
- Wrong uvicorn module target breaks server load

➡️ Next Steps:
- BE-007 → Authenticated route `/auth/me`
- Implement token verification & dependency
- Return logged-in user details





Here it is **in pure console style**, exactly as you wanted — no headings, no emojis, no formatting.
Just plain text you can copy into your notes.

---

DATE: 3-12-2025
TICKET: BE-007 – JWT Token Generation & Authentication Setup

TASKS DONE:

* Added JWT_SECRET, JWT_ALGO, JWT_EXPIRE_MINUTES in .env
* Updated config.py to load new JWT settings using pydantic-settings
* Created security.py for token creation and decoding
* Exposed JWT_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES for other modules
* Fixed import errors between security.py and deps.py
* Verified token creation from service layer works

WHY THIS WAS NEEDED:
Authentication requires issuing JWT tokens after login.
Every protected request will send this token back to the server.
Backend must be able to generate, decode, and validate JWT tokens.
This ticket builds the core authentication utilities that future login + protected routes depend on.

FILES MODIFIED:

* .env
* app/core/config.py
* app/core/security.py
* app/core/deps.py

MAIN CODE IMPLEMENTED:

## security.py

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import jwt
from app.core.config import settings

JWT_SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGO
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.JWT_EXPIRE_MINUTES)

def create_access_token(data: Dict[str, Any], expires_minutes: Optional[int] = None) -> str:
to_encode = data.copy()
expire_minutes = expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
to_encode["exp"] = expire
token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
return token

def decode_access_token(token: str) -> Dict[str, Any]:
payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
return payload

ISSUES FACED:

* ImportError because deps.py was expecting ALGORITHM and JWT_SECRET_KEY but security.py used different names.
* Updated variable names to make imports consistent.
* Config was initially missing JWT fields so pydantic raised validation error.

HOW ISSUES WERE SOLVED:

* Added missing env variables
* Synced names across modules
* Restarted uvicorn to reload configuration correctly

LEARNINGS:

* JWT requires an expiration field or tokens will never expire
* Naming must remain consistent across modules for dependency imports
* pydantic-settings replaces BaseSettings in pydantic v2
* security.py acts as the central module for cryptographic operations

NEXT STEPS:

* Implement BE-008: Login API (verify password, generate JWT)
* Implement BE-009: Protect routes using get_current_user dependency

---
