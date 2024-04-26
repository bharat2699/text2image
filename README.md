# text2image

This is a small PoC to convert prompt to image.

## Features:

- User can enter the prompt and the image will be generated asynchronously.
- The image will be stored in the S3 bucket.
- The user can download the image using the link provided.
- The user can check the status of the image generation using the requestId.
- SQLite database is used to store the image details and related Meta data.
- Celery is used to run the task asynchronously.
- Stability API is used to generate the image.

## System Requirements:

- Linux or MacOS or Windows WSL
- Python 3.8 or higher
- Redis Server
- AWS S3 Bucket with public access
- AWS IAM Role with S3 access and key pair
- Stability API Key

## How to setup:

1. Clone the repository
2. Set up .env file according to the .env.example file
3. Create a virtual environment using `python -m venv venv`
4. Install the requirements using `pip install -r requirements.txt`
5. Run migrations using `python manage.py migrate`
6. Run the server using `python manage.py runserver 8000`
7. Run the celery worker in parallel with django server using `celery -A text2image worker -l info`

## How to use:

1. CURL command for Post request to create an image:

```
curl --location 'http://127.0.0.1:8000/tti' \
--header 'Content-Type: application/json' \
--data '{
    "text": "cat playing with ball"
}'
```

2. Copy the requestId from the response of the above command.

3. CURL command for Get request to get the image using requestId:

```
curl --location 'http://127.0.0.1:8000/tti?requestId=749e3fbb-a4c7-496e-95ec-59772d61e6fc'
```

## Future Scope:

- Add failure handling for the API. using cron job to check the status of the image generation and retry.
- Add more features to the API like image type, image size, etc.
- Shifting to the better database like PostgreSQL.
- Use the AWS Lambda function to generate the image.
- Use Pub/Sub model to handle the image generation task.
