Commands run docker:
docker compose build
docker compose up

Commands for database:
docker exec -it {name} python manage.py migrate
docker cp dump-db {name}:/ 
docker exec -it {name} pg_restore -U postgres -d audio  dump-db
docker exec -it {name} python manage.py createsuperuser