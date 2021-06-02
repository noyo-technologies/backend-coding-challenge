FROM python:3.9.2

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r ./requirements.txt --no-user

CMD ["flask", "run"]
