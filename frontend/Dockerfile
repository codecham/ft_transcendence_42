FROM nginx:latest

RUN rm /etc/nginx/nginx.conf

COPY nginx.conf /etc/nginx/nginx.conf

COPY www /var/www/
COPY tools/cert.crt /etc/nginx/ssl/
COPY tools/cert.key /etc/nginx/ssl/

COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh


EXPOSE 80
EXPOSE 443

# CMD ["nginx", "-g", "daemon off;"]
# CMD ["wait-for-it.sh", "backend:8000", "--", "nginx", "-g", "daemon off;"]
CMD ["sh", "-c", "sleep 10 && nginx -g 'daemon off;'"]