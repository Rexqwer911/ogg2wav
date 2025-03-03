# Используем легковесный Python-образ
FROM python:3.9-slim

# Устанавливаем FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение в контейнер
COPY ogg2wav.py .

# Открываем порт для доступа к API
EXPOSE 8080

# Запуск приложения с gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "ogg2wav:app"]
