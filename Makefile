.PHONY: run dev up down rebuild view_logs shell-backend shell-frontend shell-db seed

# Продакшн: просто поднять в фоне
run:
	docker compose up -d

# Дев-режим: код монтируется, hot reload
dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Твой любимый "перезапусти и не закрывай"
# (останавливаем, пересобираем, поднимаем в фоне)
up:
	docker compose down || true
	docker compose up -d --build

# Остановить всё
down:
	docker compose down

# Полный пересбор
rebuild:
	docker compose down || true
	docker compose build
	docker compose up -d

# Логи всех сервисов
view_logs:
	docker compose logs -f --since 10s

# Зайти внутрь конкретных контейнеров
shell-backend:
	docker compose exec backend bash

shell-frontend:
	docker compose exec frontend bash

shell-db:
	docker compose exec db bash

seed:
	docker compose exec -T db psql -U portal -d portal < backend/sql/seed.sql