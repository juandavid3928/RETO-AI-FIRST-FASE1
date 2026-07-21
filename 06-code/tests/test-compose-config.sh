#!/usr/bin/env sh
set -eu

reserved_password='test@value:with/reserved?chars and spaces'
config=$(POSTGRES_DB=test_db POSTGRES_USER=test_user POSTGRES_PASSWORD="$reserved_password" docker compose config --format json)

COMPOSE_CONFIG="$config" EXPECTED_PASSWORD="$reserved_password" python3 -c '
import json
import os

config = json.loads(os.environ["COMPOSE_CONFIG"])
services = config["services"]
assert {"db", "backend", "frontend"} <= services.keys()
assert services["backend"]["depends_on"]["db"]["condition"] == "service_healthy"
assert services["frontend"]["depends_on"]["backend"]["condition"] == "service_healthy"
backend_environment = services["backend"]["environment"]
assert "DATABASE_URL" not in backend_environment
assert backend_environment["DB_HOST"] == "db"
assert backend_environment["DB_PASSWORD"] == os.environ["EXPECTED_PASSWORD"]
'
