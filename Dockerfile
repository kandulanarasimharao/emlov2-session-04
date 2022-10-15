#FROM python:3.9.13-slim-bullseye
FROM python:3.8.14-slim-bullseye
RUN apt update

RUN apt install -y \
    build-essential \
    git \
    curl \
    ca-certificates \
    wget \
    && rm -rf /var/lib/apt/lists

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir  -r requirements.txt
    #&& rm requirements.txt

COPY . .
#COPY src/cifar_demo_scripted.py .

#COPY logs/train/runs/2022-10-12_08-03-55/model.script.pt .

#ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3","src/cifar_demo_scripted.py","ckpt_path=model.script.pt"]
