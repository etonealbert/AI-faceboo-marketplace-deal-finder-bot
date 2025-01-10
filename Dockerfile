FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN alembic upgrade head

CMD ["python", "-m", "bot.main"]