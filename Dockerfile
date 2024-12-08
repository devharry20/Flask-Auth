FROM python:3.12.7

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

ENV FLASK_APP=app/__main__.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "-m", "app"]
