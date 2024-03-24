"""
Задание №6
📌 Создать веб-страницу для отображения списка пользователей. Приложение
должно использовать шаблонизатор Jinja для динамического формирования HTML
страницы.
📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
📌 Создайте класс User с полями id, name, email и password.
📌 Создайте список users для хранения пользователей.
📌 Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
содержать заголовок страницы, таблицу со списком пользователей и кнопку для
добавления нового пользователя.
📌 Создайте маршрут для отображения списка пользователей (метод GET).
📌 Реализуйте вывод списка пользователей через шаблонизатор Jinja.
"""

import logging
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory='templates')


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class User(UserIn):
    id: int
    # is_active: bool = False


lst_users = []
for i in range(10):
    lst_users.append(User(id=i, name=f'user0{i + 1}', email=f'user0{i + 1}mail@gmail.com',
                          password=f'{i + 1}00000'))


# print(lst_users)


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    logger.info('отработал GET запрос on main page')
    return templates.TemplateResponse('base.html', {'request': request})


# @app.get('/', response_class=HTMLResponse)
@app.get('/users/', response_class=HTMLResponse)
async def get_users(request: Request):
    logger.info('отработал GET запрос на получение списка пользователей')
    # return templates.TemplateResponse('users_bd.html', {'request': request, 'lst_users': lst_users})
    return templates.TemplateResponse('users.html', {'request': request, 'lst_users': lst_users})


@app.get('/get-users-swagger/')
async def get_users_swagger():
    logger.info('отработал GET запрос на получение списка пользователей с исп. Swagger')
    return {'lst_users': lst_users}
    # return lst_users


@app.get('/get-user-one/{id}', response_model=dict)
async def get_user_one(id: int):
    for user in lst_users:
        if user.id == id:
            logger.info('отработал GET запрос на получение инф. о пользователе по id')
            # return {'user': user}
            return user.dict()
    raise ValueError('Пользователь не найден')


@app.post('/users/add-user', response_model=User)
async def add_user_swagger(new_user: UserIn):
    new_user_id = lst_users[-1].id + 1
    new_user = User(id=new_user_id, **new_user.model_dump())
    # new_user = User(id=new_user_id, name=new_user.name, email=new_user.email, password=new_user.password)
    lst_users.append(new_user)
    logger.info('отработал POST запрос на добавление нового пользователя')
    return new_user.dict()


# @app.get("/add_user/", response_class=HTMLResponse)
# async def add_user(request: Request):
#     return templates.TemplateResponse('user_add.html', {'request': request})


@app.put('/users/update-user{usr_id}', response_model=User)
async def update_user(usr_id: int, edit_user: UserIn):
    for user in lst_users:
        if user.id == usr_id:
            user.name = edit_user.name
            user.email = edit_user.email
            user.password = edit_user.password
            logger.info(f'отработал PUT запрос на обновление пользователя')
            return user.model_dump()
    raise HTTPException(status_code=404, detail='User not found')


@app.delete("/users/delete-user/{usr_id}")
async def delete_user(usr_id: int):
    for user in lst_users:
        if user.id == usr_id:
            lst_users.remove(user)
            logger.info(f'отработал DELETE запрос на удаление пользователя')
            return lst_users
    raise HTTPException(status_code=404, detail='User not found')


if __name__ == "__main__":
    uvicorn.run("hw5_task6:app", host="127.0.0.1", port=8080)

