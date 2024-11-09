FROM python:3.10-slim

ARG ACCESS_KEY_ID
ARG SECRET_ACCESS_KEY

ENV ACCESS_KEY_ID=${ACCESS_KEY_ID}
ENV SECRET_ACCESS_KEY=${SECRET_ACCESS_KEY}

WORKDIR /backend

COPY requirements.txt /backend

RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get -y install gcc mono-mcs && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get -y install g++ mono-mcs && rm -rf /var/lib/apt/lists/*


RUN pip install dvc==3.53.2
RUN pip install dvc-s3
RUN pip install -r requirements.txt

RUN dvc get https://github.com/vkimbris/automatic-dispatching.git data/ --rev dev --remote-config access_key_id=$ACCESS_KEY_ID --remote-config secret_access_key=$SECRET_ACCESS_KEY

RUN python -m spacy download ru_core_news_sm

COPY . /backend

EXPOSE 8000

CMD ["bash", "run.sh"]

