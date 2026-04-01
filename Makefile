up:
	docker compose up --build -d

up-scaffold:
	docker compose --profile scaffold up --build -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

reset-db:
	docker compose down -v
	docker compose up --build -d

ps:
	docker compose ps
