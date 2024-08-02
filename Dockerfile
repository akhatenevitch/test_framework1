FROM mcr.microsoft.com/playwright/python:v1.38.0-jammy

WORKDIR /TestFramework

COPY . /TestFramework

RUN pip install --no-cache-dir --upgrade -r /TestFramework/requirements.txt
