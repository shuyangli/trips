# Backend server

## Local setup instructions

1. [Install docker](https://docs.docker.com/get-started/get-docker/): on Mac the easiest way is to install docker desktop.
1. Run `docker compose up`: it spins up the docker environment.
1. App will be listening at http://localhost:8000; try http://localhost:8000/healthz.

## Deployment instructions

TODO

## Postgres schema migrations

1. Create a new migration when you make changes to the models:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

2. Apply pending migrations:
   ```bash
   alembic upgrade head
   ```

3. Rollback the last migration if needed:
   ```bash
   alembic downgrade -1
   ```
