COMPOSE_FILE = docker-compose.yml

#start the database containers
start_db:
	docker-compose -f $(COMPOSE_FILE) up -d

#build the database containers
build_db:
	docker-compose -f $(COMPOSE_FILE) build

#stop the database containers
stop_db:
	docker-compose -f $(COMPOSE_FILE) down

#remove the docker database containers
clean_db: stop_db
	docker-compose -f $(COMPOSE_FILE) down --rmi all

#start the database containers
start_db_linux:
	sudo docker-compose -f $(COMPOSE_FILE) up -d

#build the database containers
build_db_linux:
	sudo docker-compose -f $(COMPOSE_FILE) build

#stop the database containers
stop_db_linux:
	sudo docker-compose -f $(COMPOSE_FILE) down

#remove the docker database containers
clean_db_linux: stop_db
	sudo docker-compose -f $(COMPOSE_FILE) down --rmi all