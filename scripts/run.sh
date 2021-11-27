docker-compose up -d

PORT="5000" \
DISCORD_WEBHOOK=$DISCORD_WEBHOOK_DEV \
MONGO_URL="mongodb://user:passw@localhost:27017/api" \
MONGO_DATA_COLLECTION="data" \
MONGO_DATA_DATABASE="api" \
MONGO_AUTH_COLLECTION="auths" \
MONGO_AUTH_DATABASE="api" \
FLASK_ENV="DEBUG" \
python gps_tracker/main.py
