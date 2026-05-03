FROM python:3.11-slim

#Hata mesajlarını anlık görme komutu
ENV PYTHONUNBUFFERED=1

# Bağımlılıkları ve CA sertifikalarını yükleme
RUN apt-get update && apt-get install -y libpq-dev gcc ca-certificates fonts-dejavu-core && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]