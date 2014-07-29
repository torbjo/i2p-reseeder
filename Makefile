.PHONY: test runserver

test:
	GET http://localhost:8080/
#	GET http://localhost:8080/ > /dev/null
#	x-www-browser http://localhost:8080/


runserver:
	python main.py netDb/
