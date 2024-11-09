FROM python:3.10-slim

ARG ACCESS_KEY_ID
ARG SECRET_ACCESS_KEY

ENV ACCESS_KEY_ID=${ACCESS_KEY_ID}
ENV SECRET_ACCESS_KEY=${SECRET_ACCESS_KEY}

WORKDIR /backend

COPY . /backend

RUN apt-get update && apt-get install -y git

RUN pip install dvc==3.53.2
RUN pip install dvc-s3

RUN dvc get https://github.com/vkimbris/automatic-dispatching.git data/ --rev dev --remote-config access_key_id=$ACCESS_KEY_ID --remote-config secret_access_key=$SECRET_ACCESS_KEY

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["bash", "run.sh"]

