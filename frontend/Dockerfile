FROM nginx:latest

RUN rm /etc/nginx/nginx.conf

COPY nginx.conf /etc/nginx/nginx.conf

COPY www /var/www/
COPY tools/cert.crt /etc/nginx/ssl/
COPY tools/cert.key /etc/nginx/ssl/

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]