FROM python:3.11-slim

WORKDIR /usr/src/app

RUN pip install numpy pandas pytest matplotlib seaborn

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

CMD ["python", "e5_2.py"]
