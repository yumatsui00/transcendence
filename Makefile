up:
	docker-compose up

down:
	docker-compose down -v

clean:
	sudo rm -rf srcs/postgres/data
	mkdir data

build:
	docker-compose up --build

logs:
	docker-compose logs -f

full clean:
	docker system prune

