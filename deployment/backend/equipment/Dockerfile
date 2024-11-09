FROM python:3.10-slim

WORKDIR /equipment

COPY . /equipment

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["bash", "run.sh"]