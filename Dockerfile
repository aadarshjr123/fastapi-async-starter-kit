FROM python:3.10-slim

WORKDIR /app

# deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# code
COPY . .

# sqlite data dir (you already map a volume)
RUN mkdir -p /app/data
ENV DATA_DIR=/app/data

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]




# explaination:
# 1. Use an official Python runtime as a parent image
# 2. Set the working directory in the container to /app (where the application code will live)
# 3. Copy the requirements.txt file into the container at /app
# 4. Install any needed packages specified in requirements.txt
# 5. Copy the rest of the application code into the container at /app
# 6. Create a directory for data storage inside the container
# 7. Set an environment variable for the data directory
# 8. Make port 8000 available to the world outside this container
# 9. Define the command to run the application using Uvicorn


# what is Uvicorn in simple terms?
# Uvicorn is a fast and lightweight web server specifically designed to run Python web applications that use the ASGI (Asynchronous Server Gateway Interface) standard. 
# It is particularly well-suited for modern web frameworks like FastAPI and Starlette, 
# which support asynchronous programming. Uvicorn helps handle incoming web requests and responses efficiently, 
# making it ideal for building high-performance web applications and APIs.

# compare it with some javascript
# In the JavaScript ecosystem, a similar role is played by web servers like Express.js or Koa.js.

# what is FastAPI in simple terms short?
# FastAPI is a modern web framework for building APIs with Python. It is designed to be fast, easy to use, and efficient,
#  allowing developers to create web applications quickly. FastAPI leverages Python's type hints to provide automatic data
#  validation and generates interactive API documentation, making it easier for developers to understand and test their APIs
#  . It is particularly well-suited for building high-performance applications that require asynchronous programming.
