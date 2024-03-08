# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=games.settings_docker
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.docker.txt

# Expose the port that Django will run on
EXPOSE 8000

# Run Django migrations and collect static files
RUN python manage.py collectstatic --noinput --settings=games.settings_docker
RUN python manage.py migrate --settings=games.settings_docker
