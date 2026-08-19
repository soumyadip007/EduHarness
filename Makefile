PYTHON ?= python3

.PHONY: install dev lint format typecheck test up down

install:
	$(PYTHON) -m pip install -r requirements.txt

dev:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

lint:
	ruff check .

format:
	black .

typecheck:
	mypy eduharness api

test:
	pytest -q

up:
	docker compose up -d

down:
	docker compose down
