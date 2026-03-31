FROM python:3.13

RUN apt-get update && apt-get install -y \
    libegl1 \
    libxkbcommon0 \
    libgl1 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

ENV PYTHONPATH=/app/src

CMD ["python", "src/main.py"]
