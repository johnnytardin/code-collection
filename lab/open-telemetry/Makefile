network:
	@if [ $(shell docker network ls -q --filter name=otlp-tests | wc -l) -eq 0 ]; then docker network create otlp-tests; fi

start: network
	@docker-compose -f docker-compose.yml up -d --build

stop:
	@docker-compose -f docker-compose.yml down

status:
	@docker-compose -f docker-compose.yml ps

clean:
	@sudo rm -rf .tmp/

restart:
	@make stop start
