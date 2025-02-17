FROM python:3.12-slim

WORKDIR /usr/src/

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /usr/src/

EXPOSE 8081

CMD ["dbt", "build"]

# CMD tail -f /dev/null