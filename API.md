### Регистрация
POST-запрос /api/v1/auth/users/
```
{
  "username": "string",
  "password": "string"
}
```
Ответ
```
{
  "email": "",
  "username": "string",
  "id": 0,
  "password": "string"
}
```

### Авторизация
POST-запрос /api/v1/auth/token/login/
```
{
  "username": "string",
  "password": "string"
}
```
Ответ
```
{
  "auth_token": "string"
}
```
Этот токен необходимо передавать в заголовке каждого запроса, в поле 
Authorization. Перед токеном должно стоять ключевое слово Token и пробел

### Создание задачи
POST-запрос /api/v1/tasks/
```
{
  "title": "string",
  "description": "string",
  "status": "new",
  "finished": "2022-08-24"
}
```
Ответ
```
{
  "id": 0,
  "author": "string",
  "title": "string",
  "description": "string",
  "created": "2021-08-24T14:15:22Z",
  "status": "new",
  "finished": "2022-08-24"
}
```

### Замена задачи
PUT-запрос /api/v1/tasks/{id}/
```
{
  "title": "string",
  "description": "string",
  "status": "new",
  "finished": "2022-08-24"
}
```
Ответ
```
{
  "id": 0,
  "author": "string",
  "title": "string",
  "description": "string",
  "created": "2021-08-24T14:15:22Z",
  "status": "new",
  "finished": "2022-08-24"
}
```

### Изменение задачи (все поля необязательные)
PATCH-запрос /api/v1/tasks/{id}/ 
```
{
  "title": "string",
  "description": "string",
  "status": "new",
  "finished": "2022-08-24"
}
```
Ответ
```
{
  "id": 0,
  "author": "string",
  "title": "string",
  "description": "string",
  "created": "2021-08-24T14:15:22Z",
  "status": "new",
  "finished": "2022-08-24"
}
```

### Удаление задачи
DELETE-запрос /api/v1/tasks/{id}/

### Получение списка задач
GET-запрос /api/v1/tasks/ 

Ответ
```
[
  {
    "id": 0,
    "author": "string",
    "title": "string",
    "description": "string",
    "created": "2021-08-24T14:15:22Z",
    "status": "new",
    "finished": "2022-08-24"
  },
  ...
]
```

### Получение задачи
GET-запрос /api/v1/tasks/{id}/

Ответ
```
{
  "id": 0,
  "author": "string",
  "title": "string",
  "description": "string",
  "created": "2021-08-24T14:15:22Z",
  "status": "new",
  "finished": "2022-08-24"
}
```

### Получение истории изменения задачи
GET-запрос /api/v1/task-history/{id}/

Ответ
```
{
  "id": 0,
  "title": "string",
  "description": "string",
  "created": "2021-08-24T14:15:22Z",
  "status": "planned",
  "finished": "2022-08-24",
  "author": "string",
  "history": [
    {
      "title": null,
      "description": null,
      "status": "planned",
      "finished": null,
      "date_change": "2021-08-24T15:15:22Z"
    },
    ...
    {
      "title": "string",
      "description": "string",
      "status": "new",
      "finished": "2022-08-25",
      "date_change": "2021-08-24T14:15:22Z"
    }
  ]
}
```