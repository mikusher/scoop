SHELL=/bin/bash


prune:
	@echo "-------- start prune ---------"
	docker-compose stop
	docker-compose down -v
	docker system prune -a --volumes -f
	@echo "-------- end prune -----------"

up:
	docker-compose up --force-recreate --build --remove-orphans --always-recreate-deps --renew-anon-volumes

up-silence:
	docker-compose up --force-recreate --build --remove-orphans --always-recreate-deps --renew-anon-volumes -d

up-debug:
	docker-compose up --force-recreate --build --remove-orphans --always-recreate-deps --renew-anon-volumes --entrypoint /bin/bash

silence:
	@echo "-------- start silence ---------"
	time docker-compose up -d
	@echo "-------- end silence -----------"

down:
	docker-compose down -v

stop:
	docker-compose stop
	docker-compose down -v