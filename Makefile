

prune:
	docker-compose down -v
	docker system prune -a --volumes -f