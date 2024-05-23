FROM python:3.8-slim-buster

WORKDIR /app
ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Run the command to start uWSGI
CMD ["flask", "run", "--host=0.0.0.0"]