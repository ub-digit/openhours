# Dockerized openhours2

The Docker specific files are located in the `docker` directory:

```
docker
├── .env.sample
├── docker-compose.yml
├── docker-entrypoint-initdb.d/
│   └── .keep
└── api/
    ├── Dockerfile
    ├── entrypoint.sh
    └── .dockerignore
```

Use your real `.env` file instead of the `.env.sample` and follow the instructions below. 
(The `docker-compose.yml` provided is the one for development.)

If you have access to the openhours2 image referred to in `docker-compose.yml`/`.env`, just follow these steps:

1. Change directory to the `docker` directory.
2. Copy your openhours2 sql dump file to `docker-entrypoint-initdb.d/`.
3. Run `docker-compose up`, if you want to run openhours2 in the foreground, or `docker-compose up -d`, if you want to run it [d]etached.

If you have to build the openhours2 image yourself, start by doing the following:

1. Change directory to the parent directory of the `docker` directory.
2. Copy `docker/api/*` to the current directory.
3. Add `docker` on a line of its own (and this `README.md` on a line of its own) in the `.dockerignore` file (optional).
4. Run `docker build -t <image-api-value-in-env-file> .` (or uncomment the build line in `docker-compose.yml`).

