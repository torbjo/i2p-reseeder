.PHONY: test runserver

test:
	GET http://localhost:8080/
#	GET http://localhost:8080/ > /dev/null
#	firefox http://localhost:8080/
#	x-www-browser http://localhost:8080/


runserver:
	python main.py /home/torkel/tmp/netDb/
