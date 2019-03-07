# Use an official Python runtime as a parent image
FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1
RUN mkdir /apps

WORKDIR /apps
COPY requirements.txt /apps
RUN pip install -r requirements.txt
COPY . /apps

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
# EXPOSE 80

# Define environment variable
# ENV NAME api

# ENV http_proxy 127.0.0.1:8000
# ENV https_proxy 127.0.0.1:8000

# ENTRYPOINT ["entrypoint"]

# Run manage.py runserver when the container launches
# CMD ["python", "manage.py", "runserver"]
