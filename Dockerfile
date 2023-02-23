FROM python:3.11.0 as dependecies

COPY requirements.txt /requirements.txt


RUN python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r /requirements.txt


FROM dependecies

COPY . /SimpleTGBot
WORKDIR /SimpleTGBot

ENV PYTHONUNBUFFERED 1

EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]