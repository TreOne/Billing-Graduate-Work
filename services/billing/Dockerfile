## Базовый образ для сборки
FROM python:3.9.10-slim as builder

WORKDIR /usr/src/app

# Запрещаем Python писать файлы .pyc на диск
ENV PYTHONDONTWRITEBYTECODE 1
# Запрещает Python буферизовать stdout и stderr
ENV PYTHONUNBUFFERED 1

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

# Установка зависимостей
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

## СБОРКА
FROM python:3.9.10-slim

# Создаем не root пользователя для проекта
RUN mkdir -p /home/app
RUN adduser --system --group app

# Создаем необходимые директории
ENV HOME=/home/app
ENV APP_HOME=/home/app/billing
ENV APP_LOGS=/home/app/billing/logs
RUN mkdir $APP_HOME
RUN mkdir $APP_LOGS
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME

# Устанавливаем зависимости
RUN apt-get update && \
    apt-get install --no-install-recommends -y netcat gettext
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Копируем точку входа
COPY --from=builder /usr/src/app/entrypoint.sh $APP_HOME

# Копируем файлы проекта
COPY ./src $APP_HOME

# Изменяем владельца файлов на app
RUN chown -R app:app $APP_HOME
RUN chown -R app:app $APP_LOGS

# Переключаемся на пользователя app
USER app
