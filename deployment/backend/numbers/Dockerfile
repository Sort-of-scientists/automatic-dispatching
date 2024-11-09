FROM python:3.10-slim

WORKDIR /numbers

COPY . /numbers

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["bash", "run.sh"]