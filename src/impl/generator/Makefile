# Generator makefile

install:
	pip install -r requirements.txt 

install-dev:
	pip install pylint nose

test:
	pylint main.py app
	nosetests tests/unit/*
	
