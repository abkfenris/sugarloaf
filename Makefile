.PHONY: docs test

help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies using pip"
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  test        run all your tests using py.test"

env:
	sudo easy_install pip && \
	pip install virtualenv && \
	virtualenv env && \
	. env/bin/activate && \
	make deps

deps:
	pip install -r requirements.txt

clean:
	python manage.py clean

lint:
	flake8 --exclude=env .

test:
	docker-compose --project-name testing -f docker-compose.test.yml up -d
	docker-compose --project-name testing -f docker-compose.test.yml run wait
	docker-compose --project-name testing -f docker-compose.test.yml run web py.test tests
	docker-compose --project-name testing -f docker-compose.test.yml down

up:
	\rm -f celerybeat.pid
	alias dc=docker-compose
	docker-compose up -d --build
	docker-compose logs -f