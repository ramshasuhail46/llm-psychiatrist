FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 7100

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["streamlit", "run", "/app/src/landingpage.py"]

# CMD ["interface.py"]
