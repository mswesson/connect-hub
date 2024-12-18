# Connect Hub - Система авторизации по номеру телефона

## Описание

Данный проект представляет собой REST API для системы авторизации пользователей по номеру телефона. API позволяет пользователям регистрироваться и входить в систему, вводя свой номер телефона и подтверждая его с помощью 4-значного кода. Каждый зарегистрированный пользователь получает уникальный инвайт-код, который можно использовать для приглашения других пользователей.

## Функционал

1. **Авторизация по номеру телефона**:

   - Пользователь отправляет запрос с номером телефона.
   - Сервер имитирует отправку 4-значного кода авторизации с задержкой 1-2 секунды.
   - Пользователь повторно отправляет запрос с номером телефона и кодом.
   - Сервер даёт токен авторизации

2. **Регистрация нового пользователя**:

   - Пользователь отправляет запрос с номером телефона.
   - Сервер имитирует отправку 4-значного кода авторизации с задержкой 1-2 секунды.
   - Пользователь повторно отправляет запрос с номером телефона и кодом.
   - Сервер создает пользователя и даёт токен авторизации

3. **Профиль пользователя**:

   - Пользователь может получить информацию о своем профиле, включая номер телефона и активированный инвайт-код.
   - При первой регистрации пользователю присваивается случайно сгенерированный 6-значный инвайт-код.

4. **Ввод чужого инвайт-кода**:

   - Пользователь может ввести инвайт-код другого пользователя.
   - Проверяется:
     - существование указанного инвайт-кода.
     - не активировал ли пользователь другйо инвайт код
     - не пригласил ли пользователь пользователя, который поделился своим инвайт кодом (замкнутый круг)
   - Каждый пользователь может активировать только один инвайт-код. Если инвайт-код уже был активирован, он отображается в профиле пользователя.

5. **Список активированных инвайт-кодов**:
   - В профиле выводится список пользователей, которые ввели инвайт-код текущего пользователя.

## API

### Регистрация

- **POST /api/register/**

  Регистрация состоит из двух шагов, запрос смс кода и ввод смс кода.

  - Запрос №1:

    ```json
    {
      "phone": "+79912345678"
    }
    ```

  - Ответ №1:

    ```json
    {
      "phone": "+79912345678",
      "sms_code": "1234"
    }
    ```

  - Запрос №2:

    ```json
    {
      "phone": "+79912345678",
      "sms_code": "1234"
    }
    ```

  - Ответ №2:

    ```json
    {
      "id": 1,
      "user_id": 1,
      "phone": "+79912345678",
      "invitation_code": "dkqjPK",
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzMTI1MDEyLCJpYXQiOjE3MzMxMjE0MTIsImp0aSI6ImI2YmIzNjQxMWI5MTRkYzk5ZmY1MWUyZWE3MDhmZjJjIiwidXNlcl9pZCI6OH0.bGnuoeniUaY1m87toHyNcqit-GG8SM12zoNpHbPrCa4"
    }
    ```

    Данный токен необходим для доступа к профилю и взаимодействию с ним.

### Авторизация пользователя

Если токен устарел, вам потребуется заного его получить.

- **POST /api/login/**

  Авторизация состоит из двух шагов, запрос смс кода и ввод смс кода.

  - Запрос №1:

    ```json
    {
      "phone": "+79912345678"
    }
    ```

  - Ответ №1:

    ```json
    {
      "phone": "+79912345678",
      "sms_code": "1234"
    }
    ```

  - Запрос №2:

    ```json
    {
      "phone": "+79912345678",
      "sms_code": "1234"
    }
    ```

  - Ответ №2:

    ```json
    {
      "id": 1,
      "phone": "+79912345678",
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzMTI1MzEyLCJpYXQiOjE3MzMxMjE3MTIsImp0aSI6ImUxYTFlMjM2Zjk0NTRlY2RiOWVhYWE3MmE1N2QwNTBlIiwidXNlcl9pZCI6OH0.EP9nBpU_WmDzGoAY1lC_V49dwPQMKN4mS41r7uwcAqU"
    }
    ```

    Данный токен необходим для доступа к профилю и взаимодействию с ним.

### Профиль пользователя

- **GET /api/clients/profile/**

  Профиль пользователя

  - Запрос:

    В профиль пользователя возможно попасть только если есть токен.
    Токен необходимо поместить в headers запроса в формате:

    `Authorization: Bearer <ваш токен>`

    Тело запроса при этом пустое.

  - Ответ:

    ```json
    {
      "id": 1,
      "phone": "+79912345678",
      "invitation_code": "dkqjPK",
      "someone_invitation_code": null,
      "connections_invited_clients": []
    }
    ```

- **PATCH /api/clients/profile/**

  Ввод чужого инвайт-кода.

  - Запрос:

    Добавить инвайт код можно только если есть токен.
    Токен необходимо поместить в headers запроса в формате:

    `Authorization: Bearer <ваш токен>`

    Тело запроса при этом:

    ```json
    {
      "invitation_code": "<6c3ESD>"
    }
    ```

  - Ответ:

    ```json
    {
      "id": 1,
      "phone": "+79912345678",
      "invitation_code": "dkqjPK",
      "someone_invitation_code": "6c3ESD",
      "connections_invited_clients": []
    }
    ```

## Установка и запуск

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/mswesson/connect-hub.git
   cd connect-hub
   ```

2. Создайте и настройте _.env_ по шаблону _.env.template_

   ```.env
   # Default settings
   SECRET_KEY= здесь ваш секретный ключ
   DEBUG= режим разработки
   ALLOWED_HOSTS= доступные адреса для входа

   # Database settings
   POSTGRES_DB= имя базы данных
   POSTGRES_USER= имя пользователя
   POSTGRES_PASSWORD= пароль базы данных
   ```

3. Установите docker и docker-compose

   Установить можно с оффициального сайта <https://docs.docker.com/engine/install/>

4. Установите poetry

   1. ```bash
      curl -sSL https://install.python-poetry.org | python3 -
      ```

   2. ```bash
      export PATH="$HOME/.local/bin:$PATH"
      ```

   3. ```bash
      source ~/.bashrc
      ```

5. Установите зависимости

   ```bash
   poetry install
   ```

6. Соберите контейнеры

   ```bash
   docker compose build
   ```

7. Запустите сервер

   ```bash
   docker compose up -d
   ```

8. API готово к работе

   API доступно по адресу <http://127.0.0.1:8000/api/>
