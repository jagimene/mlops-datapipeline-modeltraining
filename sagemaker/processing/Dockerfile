FROM python:3.8.13-slim-buster

# Copy a app folder and requirements
COPY app/ /app/
COPY requirements.txt ./

# Install libraries
RUN python -m pip install --no-cache-dir -r requirements.txt -t .

# Clean apt cache
RUN apt-get clean
   
# Set some environment variables.
# PYTHONUNBUFFERED keeps Python from buffering our standard output stream, which means that logs can be delivered to the user quickly.
# PYTHONDONTWRITEBYTECODE keeps Python from writing the .pyc files which are unnecessary in this case. 
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE 

ENTRYPOINT ["python3", "/app/processing.py"]