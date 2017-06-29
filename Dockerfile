FROM python:3.6.1
RUN apt-get update
RUN apt-get install -y g++ libssl-dev libffi-dev python3-dev
CMD ["mkdir", "-p", "/app/videos"]
WORKDIR /app
ADD youtube_downloader.py requirements.txt /app/
RUN python3 -m pip install incremental
RUN python3 -m pip install -r requirements.txt
EXPOSE 9000
CMD ["python3", "youtube_downloader.py", "-H", "0.0.0.0", "-P", "9000", "-o", "./videos"]
