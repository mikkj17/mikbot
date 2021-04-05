FROM python:3

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt
RUN apt update && apt install -y ffmpeg

CMD ["python3", "-u", "mikbot.py"]
