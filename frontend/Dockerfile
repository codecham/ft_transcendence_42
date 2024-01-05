# FROM nginx:latest

# RUN rm /etc/nginx/nginx.conf

# COPY nginx.conf /etc/nginx/nginx.conf

# COPY www /var/www/
# COPY tools/cert.crt /etc/nginx/ssl/
# COPY tools/cert.key /etc/nginx/ssl/

# COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
# RUN chmod +x /usr/local/bin/wait-for-it.sh


# EXPOSE 80
# EXPOSE 443

# CMD ["sh", "-c", "sleep 10 && nginx -g 'daemon off;'"]

# Utilisation de l'image Debian Buster
FROM debian:buster

# Installation de NGINX
RUN apt-get update && apt-get install -y nginx

# Suppression du fichier de configuration par défaut
RUN rm /etc/nginx/nginx.conf

# Copie du fichier de configuration personnalisé
COPY nginx.conf /etc/nginx/nginx.conf

# Copie des fichiers du site web
COPY www /var/www/

# Copie des fichiers du certificat SSL
COPY tools/cert.crt /etc/nginx/ssl/
COPY tools/cert.key /etc/nginx/ssl/

# Copie du script wait-for-it
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Exposition des ports 80 et 443
EXPOSE 80
EXPOSE 443

# Commande d'exécution de NGINX
CMD ["sh", "-c", "/var/www/get_ip.sh && mv host_ip.json /var/www/ && sleep 10 && nginx -g 'daemon off;'"]
