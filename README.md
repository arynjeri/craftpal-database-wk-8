# 📦 CraftPal API

A simple CRUD API built with **FastAPI** and **MySQL** to manage craft-related data.
Includes endpoints for managing **Users** and **Projects**.

---

## 🚀 Features

* FastAPI backend with MySQL database
* Full CRUD operations for:

  * `Users`
  * `Projects`
* Interactive API documentation at `/docs`

---

## ⚙️ Requirements

* Python 3.10+
* MySQL Server installed locally
* Packages from `requirements.txt`

```txt
fastapi==0.116.1
uvicorn==0.35.0
mysql-connector-python==9.4.0
pydantic==2.11.9
python-dotenv==1.0.1
```

---

## 💻 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/craftpal.git
cd craftpal
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```

* **Windows**

  ```bash
  venv\Scripts\activate
  ```
* **Mac/Linux**

  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configure the Database

1. Make sure MySQL server is running.
2. Create the database and tables:

```sql
CREATE DATABASE craftpal;

USE craftpal;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    bio TEXT
);

CREATE TABLE Projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
```

3. Create a `.env` file in the project root with your credentials:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=craftpal
```

---

## ▶️ Running the App

**Using Uvicorn:**

```bash
uvicorn app:app --reload
```

The app will run at:
🔗 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📑 API Documentation

Swagger UI is available at:
🔗 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📁 Project Structure

```
craftpal/
│
├── app.py            # Main FastAPI app with CRUD routes
├── database.py       # MySQL connection (optional)
├── .env              # Database credentials
├── requirements.txt  # Project dependencies
└── README.md
```

---

## 📌 API Endpoints

### **Users**

| Method | Endpoint      | Description             |
| ------ | ------------- | ----------------------- |
| POST   | `/users`      | Create a new user       |
| GET    | `/users`      | Get all users           |
| GET    | `/users/{id}` | Get a single user by ID |
| PUT    | `/users/{id}` | Update a user by ID     |
| DELETE | `/users/{id}` | Delete a user by ID     |

### **Projects**

| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| POST   | `/projects`      | Create a new project       |
| GET    | `/projects`      | Get all projects           |
| GET    | `/projects/{id}` | Get a single project by ID |
| PUT    | `/projects/{id}` | Update a project by ID     |
| DELETE | `/projects/{id}` | Delete a project by ID     |

---

## ✨ Example Requests

### Create a User

```json
POST /users
{
  "name": "Alice",
  "username": "alice123",
  "email": "alice@example.com",
  "password": "securepass",
  "bio": "Craft enthusiast"
}
```

### Update a User

```json
PUT /users/1
{
  "name": "Alice Smith",
  "username": "alice123",
  "email": "alice@example.com",
  "password": "newpass123",
  "bio": "Updated bio"
}
```

### Create a Project

```json
POST /projects
{
  "title": "Crochet Tote Bag",
  "description": "Handmade crochet bag with floral design",
  "user_id": 1
}
```

### Update a Project

```json
PUT /projects/1
{
  "title": "Knitted Tote Bag",
  "description": "Updated project description",
  "user_id": 1
}
```
