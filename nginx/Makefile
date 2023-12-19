#REPLACE BY YOUR ABOSLUTE PATH 
CONF_PATH = /Users/corentin/Desktop/19/ft_transcendence_local/nginx/nginx.conf

all: 
	sudo nginx -c $(CONF_PATH)

stop: 
	sudo nginx -s stop

re: 
	sudo nginx -s reload

update:
	sudo rm -rf /var/www/*
	sudo cp -R ../frontend/* /var/www/
	sudo chmod -R 777 /var/www/
