FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY flask-starter/templates/ ./flask-starter/templates/
COPY logic/ ./logic/
COPY routes/ ./routes/
COPY wsgi.py .

ENV PYTHONUNBUFFERED=1
EXPOSE 3000

CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-3000} app:app"]