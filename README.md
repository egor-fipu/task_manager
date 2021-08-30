## Техническое задание:

Персонализированный сервис task manager, позволяющий пользователю ставить себе 
задачи, отражать в системе изменение их статуса и просматривать историю задач.

Сервис предоставляет интерфейс в виде JSON API, это единственный способ общения клиента с сервисом
Авторизация в апи происходит с помощью токена (переданного в заголовке Authorization)
сервис покрыт тестами


### Функциональные требования:

   1. Пользователь может зарегистрироваться в сервисе задав пару логин-пароль
   2. В системе может существовать много пользователей
   3. Пользователь может авторизоваться в сервисе предоставив пару логин-пароль и получив в ответе токен
   4. Пользователь видит только свои задачи
   5. Пользователь может создать себе задачу. Задача должна как минимум содержать следующие данные (* - обязательные поля):
      - *Название
      - *Описание
      - *Время создания
      - *Статус - один из: Новая, Запланированная, в Работе, Завершённая
      - Планируемая дата завершения

   6. Пользователь может менять статус задачи на любой из данного набора
   7. Пользователь может менять планируемое время завершения, название и описание
   8. Пользователь может получить список своих задач, с возможностью фильтрации по статусу и планируемому времени завершения
   9. Пользователь может просмотреть историю изменений задачи (названия, описания, статуса, времени завершения)


### Запуск проекта в dev-режиме

- Установить и активировать виртуальное окружение
- Установить зависимости из файла requirements.txt

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
``` 

- Выполнить миграции:

```bash
python manage.py migrate
```


- Запустить проект:

```bash
python manage.py runserver
```

- Запуск тестов
```bash
python manage.py test
```

### Документация API

После запуска доступна в форматах:

- [Swagger](http://127.0.0.1:8000/swagger/)
- [ReDoc](http://127.0.0.1:8000/redoc/)