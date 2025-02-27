FROM python:3.12.1-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate && python manage.py loaddata db_fixture.json

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]