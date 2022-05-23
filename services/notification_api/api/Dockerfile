## БАЗОВЫЙ ОБРАЗ
FROM python:3.9.10-slim AS builder-image
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

# Установка зависимостей
COPY /requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


## СБОРКА
FROM python:3.9.10-slim

# Создаем пользователя
RUN mkdir -p /home/app
RUN adduser --system --group app

# Создаем переменные окружения
ENV PYTHONUNBUFFERED 1
ENV HOME=/home/app
ENV APP_HOME=/home/app/src
ENV APP_LOGS=/home/app/logs

# Создаем необходимые директории
RUN mkdir $APP_HOME
RUN mkdir $APP_LOGS
WORKDIR $APP_HOME

# Устанавливаем зависимости
COPY --from=builder-image /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Копируем файлы проекта
COPY /src/ $APP_HOME

# Изменяем владельца файлов на app
RUN chown -R app:app $APP_HOME
RUN chown -R app:app $APP_LOGS

# Переключаемся на пользователя app
USER app

# Запускаем скрипт
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
