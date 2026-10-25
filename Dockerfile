FROM python:3.11-slim

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    xvfb \
    libpq-dev \
    python3-dev \
    wget \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

# Создаём папки для данных (если их нет)
RUN mkdir -p data images/photos keys video

# Запуск через xvfb
CMD ["xvfb-run", "--auto-servernum", "--server-args=-screen 0 1920x1080x24", "python", "main.py"]