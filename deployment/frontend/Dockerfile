FROM python:3.10-slim

WORKDIR /numbers

COPY requirements.txt /numbers

RUN pip install -r requirements.txt

COPY . /numbers

EXPOSE 8000

CMD ["bash", "run.sh"]