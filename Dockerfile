FROM python:3

ENTRYPOINT ["tail", "-f", "/dev/null"]

RUN apt-get update && apt-get install -y \
    chromium \
    xvfb \
    ffmpeg

ENV DISPLAY=:0



WORKDIR /app

COPY . .

# RUN pip install -r requirements.txt --force

# CMD ["python3", "main.py", "-f", "--ignore-time"]

# CMD ["Xvfb", ":0", "-screen", "0", "1024x768x16"] && chromium