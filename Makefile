makemigrations:
	docker compose exec app python manage.py makemigrations
migrate:
	docker compose exec app python manage.py migrate