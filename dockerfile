FROM python:3.9
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx  tesseract-ocr

COPY . /app

# RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt