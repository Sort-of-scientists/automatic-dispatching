FROM python:3.10-slim

WORKDIR /multilabel

COPY . /multilabel

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["bash", "run.sh"]