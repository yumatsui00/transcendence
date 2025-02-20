all: up

up: 
	docker compose -f ./docker-compose.yml up

build:
	docker compose -f ./docker-compose.yml build

down:
	docker compose -f ./docker-compose.yml down

stop:
	docker compose -f ./docker-compose.yml stop

clean:
	docker rmi transcendence-nginx transcendence-django transcendence-postgres transcendence-dbeaver

fclean:
	sudo rm -rf ./srcs/2FA/2FA_DB/data ./srcs/Authenticator/Auth_DB/data ./srcs/User-management/User_DB/data ./srcs/RootCA/certs