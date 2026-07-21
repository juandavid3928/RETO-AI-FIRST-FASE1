#!/usr/bin/env sh
set -eu

config=$(POSTGRES_DB=test_db POSTGRES_USER=test_user POSTGRES_PASSWORD=test_password docker compose config)

printf '%s' "$config" | grep -q '^  backend:'
printf '%s' "$config" | grep -q '^  db:'
printf '%s' "$config" | grep -q '^  frontend:'
printf '%s' "$config" | grep -q 'condition: service_healthy'
printf '%s' "$config" | grep -q 'restart: true'
