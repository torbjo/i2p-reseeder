
.PHONY: all

test:
	GET http://localhost:8080/ > /dev/null

all:
	firefox http://localhost:8080/
	#x-www-browser http://localhost:8080/


runserver:
	python main.py /home/torkel/tmp/netDb/
