FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD alembic upgrade head && python -m src.load