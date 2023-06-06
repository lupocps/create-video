FROM python:3 AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y libffi-dev gcc

ADD . /app
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --target=/app -r requirements.txt


# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10


COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
# Pass the repository secret as an environment variable
ENV LUPO_CORE_AZURE_STORAGE_CONNECTION_STRING=${LUPO_CORE_AZURE_STORAGE_CONNECTION_STRING}

CMD ["/app/main.py"]