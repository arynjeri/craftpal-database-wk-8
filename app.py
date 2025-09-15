from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Create a reusable function to connect to the DB
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

#  Pydantic Models
class User(BaseModel):
    name: str
    username: str
    email: str
    password: str
    bio: str | None = None

class Project(BaseModel):
    title: str
    description: str | None = None
    user_id: int

#  Test Connection
@app.get("/")
def test_connection():
    """Check database connection and list tables."""
    try:
        db = get_db_connection()
        cur = db.cursor(dictionary=True)
        cur.execute("SHOW TABLES")
        tables = [row[f"Tables_in_{db.database}"] for row in cur.fetchall()]
        cur.close()
        db.close()
        return {"message": "Connected successfully", "tables": tables}
    except Exception as e:
        return {"message": "Connection failed", "error": str(e)}

#  USERS CRUD
@app.post("/users")
def create_user(user: User):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO Users (name, username, email, password, bio) VALUES (%s,%s,%s,%s,%s)",
        (user.name, user.username, user.email, user.password, user.bio)
    )
    db.commit()
    cur.close()
    db.close()
    return {"message": "User created successfully"}

@app.get("/users")
def get_users():
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Users")
    users = cur.fetchall()
    cur.close()
    db.close()
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    db.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        "UPDATE Users SET name=%s, username=%s, email=%s, password=%s, bio=%s WHERE id=%s",
        (user.name, user.username, user.email, user.password, user.bio, user_id)
    )
    db.commit()
    affected_rows = cur.rowcount
    cur.close()
    db.close()

    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("DELETE FROM Users WHERE id=%s", (user_id,))
    db.commit()
    affected_rows = cur.rowcount
    cur.close()
    db.close()

    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}

#  PROJECTS CRUD 
@app.post("/projects")
def create_project(project: Project):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO Projects (title, description, user_id) VALUES (%s,%s,%s)",
        (project.title, project.description, project.user_id)
    )
    db.commit()
    cur.close()
    db.close()
    return {"message": "Project created successfully"}

@app.get("/projects")
def get_projects():
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Projects")
    projects = cur.fetchall()
    cur.close()
    db.close()
    return projects

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM Projects WHERE id = %s", (project_id,))
    project = cur.fetchone()
    cur.close()
    db.close()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}")
def update_project(project_id: int, project: Project):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute(
        "UPDATE Projects SET title=%s, description=%s, user_id=%s WHERE id=%s",
        (project.title, project.description, project.user_id, project_id)
    )
    db.commit()
    affected_rows = cur.rowcount
    cur.close()
    db.close()

    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"message": "Project updated successfully"}

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("DELETE FROM Projects WHERE id=%s", (project_id,))
    db.commit()
    affected_rows = cur.rowcount
    cur.close()
    db.close()

    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"message": "Project deleted successfully"}

# Run the app 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
