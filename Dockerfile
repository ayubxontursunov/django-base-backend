# pull official base image
FROM python:3.11.5

# set work directory
WORKDIR /home/app/web

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# install system dependencies
RUN apt-get update && apt-get install -y gettext libreoffice netcat-traditional

# install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project
COPY . /home/app/web/

# create standard directories
RUN mkdir -p /home/app/web/static /home/app/web/media /home/app/web/locale

# Make entrypoint executable
RUN chmod +x /home/app/web/entrypoint.sh

# set entrypoint
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
