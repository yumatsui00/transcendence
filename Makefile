up:
	docker-compose up

down:
	docker-compose down -v

build:
	docker-compose up --build

logs:
	docker-compose logs -f

full clean:
	docker system prune

