FROM python:3.10-slim

WORKDIR /database

COPY requirements.txt /database

RUN pip install --no-cache-dir -r requirements.txt

COPY . /database

EXPOSE 8000

CMD ["bash", "run.sh"]