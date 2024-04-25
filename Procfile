release: python manage.py migrate
web: python -m uvicorn games.asgi:application --port $PORT --host 0.0.0.0
