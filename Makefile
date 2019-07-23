# Installation directivces for 

all:
	install

install: 
	echo "nothing done"

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '__pycache__' -exec rm -R --force {} +

run:	clean
	python application.py

test:	clean
	python ./app/tests/run_tests.py

docker-mongo:
	sudo docker pull mongo
	sudo docker network create h2hapi
	sudo docker stop h2hdb-mongo
	sudo docker rm h2hdb-mongo
	sudo docker run --name h2hdb-mongo -d -p 27017:27107 -v ~/data:/data/db mongo
	sudo docker run --entrypoint mongod --hostname h2hdb --name h2hdb-mongo -d -p 27017:27107 -v ~/data:/data/db mongo