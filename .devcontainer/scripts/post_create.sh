#!/usr/bin/env bash

# Start Postgres
docker compose --file contrib/docker-compose-postgres.yml up --detach

# Upgrade Pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.dev.txt
