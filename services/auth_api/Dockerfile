ARG PYTHON_VERSION=3.9.10-slim
FROM python:${PYTHON_VERSION} as python

## Базовый образ для сборки
FROM python as python-build-stage

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1

# Устанавливаем зависимости
RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc netcat dos2unix && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем точку входа
COPY entrypoint.sh .
# Fix права на выполнение (для пользователей unix систем)
RUN ["chmod", "+x", "entrypoint.sh"]
# Fix окончания строк (для пользователей win систем)
RUN dos2unix entrypoint.sh

# Проверка оформления кода
RUN pip install --upgrade pip
RUN pip install flake8
COPY /src .
RUN flake8 --ignore=W503,E501,F401,E231 .

# Установка зависимостей
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


## СБОРКА
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Создаем не root пользователя для проекта
RUN mkdir -p /home/app
RUN adduser --system --group app

# Создаем необходимые директории
ENV HOME=/home/app
ENV APP_HOME=/home/app/src
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Устанавливаем зависимости
RUN apt-get update && \
    apt-get install --no-install-recommends -y netcat
COPY --from=python-build-stage /usr/src/app/wheels /wheels
COPY --from=python-build-stage /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Копируем точку входа
COPY --from=python-build-stage /usr/src/app/entrypoint.sh $HOME

# Копируем файлы проекта
COPY /src/auth_api $APP_HOME/auth_api
COPY /src/auth_api/migrations $APP_HOME/migrations

# Изменяем владельца файлов на app
RUN chown -R app:app $APP_HOME

# Переключаемся на пользователя app
USER app
