#Шаблонизатор Jinja 2

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Убедитесь, что папка 'templates' существует

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# Список пользователей
users = []

# Создание пользователя
def create_user(username: str, age: int):
    user_id = (users[-1].id + 1) if users else 1  # Генерация ID
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

# Запрос для отображения списка пользователей
@app.get("/", response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {
        "request": request,
        "users": users,
        "title": "Users List"  # Добавьте нужные ключи в соответствии с вашим шаблоном
    })

# Запрос для отображения информации о конкретном пользователе
@app.get("/user/{user_id}", response_class=HTMLResponse)
async def read_user(request: Request, user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {
        "request": request,
        "user": user,
        "title": f"User: {user.username}"  # Добавьте дополнительные ключи для шаблона
    })

# Создание пользователей при запуске приложения
@app.on_event("startup")
async def startup_event():
    create_user("UrbanUser", 24)
    create_user("UrbanTest", 22)
    create_user("Capybara", 60)