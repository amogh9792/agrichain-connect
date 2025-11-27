------------------------------------------------------------
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
------------------------------------------------------------


------------------------------------------------------------

# 📅 Date: 27-11-2025

# 🎫 Tickets Worked On:
- **BE-002 – Database Setup, Environment Fixes & Alembic Initialization**

------------------------------------------------------------

# 📝 Today's Tasks:

- Added `docker-compose.yml` to run PostgreSQL using Docker  
- Created `.env` file for storing DB username & password securely  
- Installed and configured **SQLAlchemy** (ORM)  
- Installed and configured **Alembic** for database migrations  
- Fixed Windows PostgreSQL service conflict  
- Ensured Docker PostgreSQL is the only active database  
- Successfully created & applied initial Alembic migration  

------------------------------------------------------------


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

------------------------------------------------------------

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

------------------------------------------------------------

# 📂 Files Modified:

- **docker-compose.yml**
- **.env**
- **alembic.ini**
- **alembic/env.py**
- **.gitignore**
- Initial migration in `alembic/versions/`

------------------------------------------------------------

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

------------------------------------------------------------

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

------------------------------------------------------------

# 📚 Learnings:

- Only **one** process can use port 5432.  
- Docker PostgreSQL is safer and isolated from OS conflicts.  
- `.env` keeps passwords hidden and secure.  
- Alembic is essential for keeping DB changes in sync.  
- SQLAlchemy + Alembic is industry-standard for Python projects.  
- Docker volumes store data persistently even after container restarts.  
- Migrations prevent “works on my PC” database issues.

------------------------------------------------------------

# ➡️ Next Steps:

- Start **BE-003 – Application Bootstrap**
  - Create `main.py`
  - Add `/health` route
  - Setup router structure
  - Connect DB session with FastAPI

------------------------------------------------------------


