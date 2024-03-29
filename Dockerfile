FROM python:3

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "-u", "-m", "mikbot.main"]
