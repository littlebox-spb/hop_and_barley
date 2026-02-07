FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    g++ \
    python3-dev \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.1.1
RUN pip install poetry==2.1.1

ENV PATH="/root/.local/bin:$PATH"
ENV SECRET_KEY="django-insecure-0x3%*k!%6^8)0#4m%+j&+&6b0$g%&r!^2@^)g%&4!4$!&t4"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]