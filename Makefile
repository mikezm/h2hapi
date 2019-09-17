# Installation directivces for 

all:
	install

install: 
	echo "nothing done"

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '__pycache__' -exec rm -R --force {} +

run:
	sls wsgi serve

test:
	python ./app/tests/run_tests.py