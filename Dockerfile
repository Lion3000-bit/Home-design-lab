FROM python:3.11-slim

# Устанавливаем рабочую папку внутри контейнера
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Сначала копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код проекта
COPY . .

# Открываем порт наружу
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
