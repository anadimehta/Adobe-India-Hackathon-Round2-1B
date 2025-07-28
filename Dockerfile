FROM --platform=linux/amd64 python:3.10

WORKDIR /app

# Copy all code into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set the entrypoint to use parser.py
CMD ["python", "parser.py", "--all"]