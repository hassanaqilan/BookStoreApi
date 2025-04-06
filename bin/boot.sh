#!/usr/bin/env bash

set -e

BIN_ROOT=$(dirname $0)

#alembic upgrade head
PYTHONPATH=$(pwd) alembic -c book_store_api/alembic.ini upgrade head

uvicorn --reload --workers 1 --host 0.0.0.0 --port 80 app:app

