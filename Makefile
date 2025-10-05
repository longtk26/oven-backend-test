newmg:
	uv run python manage.py makemigrations 
mgup:
	uv run python manage.py migrate
run:
	uv run python manage.py runserver
test:
	uv run python manage.py test

