FROM python:3.10-slim

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

EXPOSE 8000

COPY . /multilabel
WORKDIR /multilabel

CMD ["bash", "run.sh"]