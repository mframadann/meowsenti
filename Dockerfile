FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/nltk_data
ENV NLTK_DATA=/app/nltk_data

RUN python -m nltk.downloader -d /app/nltk_data stopwords

COPY . .

EXPOSE 7860

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:7860"]
