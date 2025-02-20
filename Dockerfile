# Use the official Python image as the base image
FROM python:3.9-slim
# Set the working directory in the container
WORKDIR /app
# Copy the re.txt first to leverage Docker cache
# (Make sure you create a requirements.txt file with necessary dependencies)
COPY re.txt /app/
# Install the required dependencies
RUN pip install --no-cache-dir -r re.txt
# Copy the entire app into the container
COPY . /app/
# Expose the port that FastAPI will run on
EXPOSE 8000
# Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
