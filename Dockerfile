FROM python:3.8.10

WORKDIR /src

COPY . /src

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]