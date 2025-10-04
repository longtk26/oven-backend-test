newapp:
	uv run python manage.py startapp ${name}
newmg:
	uv run python manage.py makemigrations ${name}
mgup:
	uv run python manage.py migrate
run:
	uv run python manage.py runserver

