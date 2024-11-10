FROM python:3.10-slim

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

WORKDIR /equipment
COPY . /equipment

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apt-get update && apt-get upgrade -y && apt-get install -y git

RUN pip install dvc dvc-s3

RUN dvc get https://github.com/vkimbris/automatic-dispatching.git --rev equipment-model@v0.0.1 models/final-model.pt --remote-config access_key_id=YCAJEk1Dap7upINca7OgHQ2MM --remote-config secret_access_key=YCMEeVSyCwieGkX2JfbJWRnrnhzpHjsmej4OqUXb

EXPOSE 8000

CMD ["bash", "run.sh"]