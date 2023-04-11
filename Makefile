.PHONY: build deploy dev update

build:
	docker-compose build
	docker push registry.crdn.kz/crdn-parser

deploy:
	docker-compose pull
	docker-compose up -d

dev:
	docker-compose up -d --build

update:
	git pull
