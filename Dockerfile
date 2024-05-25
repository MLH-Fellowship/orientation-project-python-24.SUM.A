FROM python:3.11

WORKDIR /app
ADD . /app

# install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Run the command to start uWSGI
CMD ["flask", "run", "--host=0.0.0.0"]