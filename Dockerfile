FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime

WORKDIR /app
COPY . .
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 nano -y
RUN pip3 install -r requirements.txt
CMD ["python3", "bot.py"]
