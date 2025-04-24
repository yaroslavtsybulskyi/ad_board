FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get install -y build-essential libpq-dev curl netcat-openbsd \
  && pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . .

RUN mkdir -p /vol/web/media/ vol/web/static


ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]