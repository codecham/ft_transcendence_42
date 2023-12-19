# SETUP
1) install nginx on your os
2) Check if you have a directory named "/var/www/". If not create it
3) Replace the value of CONF_PATH in the makefile by the absolute path where the nginx.conf is. Basicly is the path of the project here + /nginx/nginx.conf
4) Do a make update (That will push the content of frontend into the /var/www/)

# USAGE
1) For start NGINX just use make
2) For stop NGINX just use make stop
3) For reload NGINX just use make reload
4) For update changes that you do just use make update
