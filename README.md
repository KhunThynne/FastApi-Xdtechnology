# FastApi-Thynne 🚀
Version: 0.1.1
FastAPI backend project for Thynne, incorporating API, GraphQL, and various services.

## 📦 Features

- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.12+.
- **GraphQL**: Integrated using Strawberry to provide a flexible and efficient alternative to REST.
- **Async**: Fully asynchronous support for high concurrency.
- **Type Safety**: Utilizes Python type hints for better code quality and developer experience.

## 🛠️ Requirements

- [Python 3.12+](https://www.python.org/downloads/)
- [Virtualenv](https://docs.python.org/3/library/venv.html) or [Poetry](https://python-poetry.org/)

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/KhunThynne/fastapi-thynne.git
cd FastApi-Thynne
```

### 2. Set up a virtual environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows (Command Prompt)
venv\Scripts\activate.bat
# Windows (PowerShell)
venv\Scripts\Activate.ps1
# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application
create .env and add DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres" <- your database url
You can use the provided batch script or run it manually.

**Using the batch script (Windows):**
bump-my-version bump major --commit --tag
bump-my-version bump minor --commit --tag
bump-my-version bump patch --commit --tag
```cmd
run.bat
```

**Manually:**

```bash
./run.bat
# Ensure your PYTHONPATH includes the src directory
set PYTHONPATH=%CD%\src  # Windows
export PYTHONPATH=$PWD/src # Mac/Linux

# Run the Uvicorn server
python -m src.main
```

The server will start at `http://127.0.0.1:8000`.

## 📚 Documentation

- **Swagger UI**: Visit `http://127.0.0.1:8000/docs` for the interactive API documentation.
- **ReDoc**: Visit `http://127.0.0.1:8000/redoc` for an alternative API documentation view.
- **GraphQL Playground**: Visit `http://127.0.0.1:8000/graphql` to explore and query the GraphQL API.

## 🧪 GraphQL Examples

### Query: Get All Users

```graphql
query {
  getUsers {
    id
    username
    email
  }
}
```

### Mutation: Create User

```graphql
mutation {
  createUser(username: "newuser", email: "new@example.com") {
    id
    username
    email
  }
}
```
