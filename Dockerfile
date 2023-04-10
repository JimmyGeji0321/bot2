# Use the official Python image as the base image
FROM --platform=linux/amd64 python

# Copy the chatbot.py and requirements.txt files to the container
COPY chatbot.py .
COPY requirements.txt .
COPY config.ini .

# Install the required dependencies
RUN pip install -r requirements.txt

# Set the environment variables
ENV ACCESS_TOKEN=6082859744:AAFKILnGHEtVz2kxkc7_X4XGp3LEH5rlrSw
ENV HOST=redis-11411.c1.us-east1-2.gce.cloud.redislabs.com
ENV PASSWORD=QsBDWgtvzq5mUfTZjUi6oWaxZtLnm32R
ENV REDISPORT=11411

# Set the entrypoint to run the chatbot.py script
ENTRYPOINT ["python", "chatbot.py"]