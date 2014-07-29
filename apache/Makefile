# Use this to generate apache.conf from apache.conf.in

#DOMAIN=i2p-netdb.innovatio.no
PREFIX=/srv/www/$(DOMAIN)

all: apache.conf

% : %.in
	@if [ x$(DOMAIN) = x ]; then \
	    echo "Error: Missing domain name!" ;\
	    echo "usage: Make DOMAIN=normal.no [PREFIX=/srv/www/normal.no]" ;\
	    false ;\
	fi
	sed -e 's|@DOMAIN@|$(DOMAIN)|g' \
	    -e 's|@PREFIX@|$(PREFIX)|g' < $< > $@
