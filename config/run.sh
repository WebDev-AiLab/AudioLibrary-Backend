#!/usr/bin/env sh

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createcachetable

# create superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@agrachyov.com', 'password') if not User.objects.filter(username='admin').exists() else False" | python manage.py shell

# temporary
python manage.py runscript quick_import_csv
python manage.py runscript generate_initial_data

# be careful with workers and threads
gunicorn audiolibrary_django.wsgi:application --bind 0.0.0.0:8000 --timeout 600 --workers 2 --threads 4