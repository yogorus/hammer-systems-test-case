# Тестовое задание на позицию python разработчика
## Cсылка на ТЗ
> https://disk.yandex.ru/i/-t5XQ6cmWkNNxQ

## Деплой
1. Нужно скопировать содержимое **.env.example** в файл **.env** и наполнить его кредами. Ну или оставить как есть.
2. Собрать контейнеры
    > docker-compose up -d

# Postman
Нужно экспортировать коллекцию и окружение к себе. Всё лежит в папке postman

## API-эндпоинты
Все адреса API имеют префикс **api/v1/**. Дальше перечислено то, что идет после него

### 1. /phone_auth/
Здесь мы вводим номер телефона и получаем в ответ код, который нужно будет активировать в другом эндпоинте.

Сервер проверит, есть ли пользователь с таким номером в БД, и в таком случае, не даст зарегистрироваться этим номером.

В качестве имитации проверки номера и кода верификации номер и код сохраняются в куки пользователя, потом они будут проверены в следующем эндпоинте.

### 2. /register/
В этом эндпоинте мы вводим 4-значный код, сгенерированный ранее. Если введенный код совпадает с тем, что хранится в куки, то пользователь добавляется в БД

Помимо этого, автоматически создается реферальный код

### 3. /user/<pk>/
Эндпоинт для просмотра профиля юзера, активации реферального кода и удаления(сделал для тестов)

В адресную строку нужно подавать **id** юзера

**Методы**:

- **GET**
> Сервер дает ответ в виде данных пользователя, какой реферальный код он активировал и список пользователей, которые активировались по его коду(в ключе **"referral"**).

- **PUT**
> Сервер принимает на вход параметр **code**, после чего делает дальнейшие необходимые проверки. В случае успеха, пользователь становится активированным(**is_activated**) и больше не может использовать коды активации. Также заполняется параметр **invited_by**, показывающий каким кодом активировался пользователь.
