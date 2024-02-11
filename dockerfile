# argument from makefile to set type of arch
ARG ARCH

FROM ${ARCH}/python:3.13-rc-slim

# Set the working directory in the container
WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ARG OPENIA_TOKEN

ENV OPENIA_TOKEN=${OPENIA_TOKEN}:-default_value}

# Run app.py when the container launches
CMD ["python", "src/main.py"]
