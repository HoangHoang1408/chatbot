poetry export --without-hashes --format=requirements.txt --output=requirements.txt
docker build -t custom_service_chatbot:v0.1