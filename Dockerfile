# base image (host os) -> python3.8.10
FROM python:3.8.10

# environment variables [required]
ARG DATABASE_NAME 
ARG DATABASE_USER 
ARG DATABASE_PASSWORD
ARG DATABASE_PORT
ARG DATABASE_HOST
ARG ENDPOINT_URL
ARG DESTINATION_BUCKET_NAME
ARG SIGNATURE_VERSION 
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY 
ARG MAX_NUMBER_BACKUPS 
ARG SCHEDULE

ENV TEMP_DIR_STORE_FILES 'temp_dir'

# working directory in the container
WORKDIR /project

# copy requirements files to /project
COPY requirements.txt .

# install libraries and dependencies
RUN mkdir ${TEMP_DIR_STORE_FILES}
RUN apt-get update
RUN apt-get -y install postgresql-client
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy the /src content into the /project
COPY src/ .

# run main.py to start the project
CMD [ "python", "./main.py" ]