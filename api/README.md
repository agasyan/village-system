# API

If you haven't installed postgres run this
```
sudo apt-get install postgresql
sudo service postgresql start
sudo passwd postgres
sudo apt-get install --reinstall libpq-dev
```

Installing
```bash
python3 -m venv env
source env/bin/activate

```

This used for compiling `psycopg2` if you want to run it on local development

## Run alembic
To update after model changes
Run PSQL first
```
docker-compose up -d dtpl-db
```

```
docker-compose run api alembic revision --autogenerate
```
Migrate
```
docker-compose run api alembic upgrade head
```

connect to db
```
psql -U postgres -h localhost -p 5436
```

See docs
```
localhost:5000/docs
```

Install new dependencies / library
```
pip freeze > requirements.txt 
```