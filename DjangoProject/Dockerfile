FROM python:3.11.5-slim-bullseye

# Встановлення базових системних інструментів і бібліотек
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    default-libmysqlclient-dev \
    pkg-config \
    postgresql-client

# Очистка кешу apt
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Налаштування середовища Python
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Робоча директорія
WORKDIR /app

# Копіюємо залежності
COPY requirements.txt .

# Встановлення Python-залежностей
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо решту коду
COPY . .

# Вказуємо команду для запуску
CMD ["python", "adddb.py"]
