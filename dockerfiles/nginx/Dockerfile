FROM nginx:latest
ADD nginx.conf /etc/nginx/nginx.conf
RUN openssl req -nodes -x509 -newkey rsa:4096 -sha256 -keyout /etc/nginx/key.pem -out /etc/nginx/cert.crt -days 1095 -subj "/C=US/ST=Oregon/L=Portland/O=IT"