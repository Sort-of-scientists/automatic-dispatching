FROM python:3.10-slim

WORKDIR /backend

COPY . /backend

RUN pip install dvc==3.53.2
RUN pip install dvc-s3

RUN pip install -r requirements.txt

RUN python -m spacy download ru_core_news_sm

EXPOSE 8000

CMD ["bash", "run.sh"]

