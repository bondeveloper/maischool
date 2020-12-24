# FROM nginx:latest
FROM nginxinc/nginx-unprivileged:1-alpine

# RUN rm /etc/nginx/conf.d/default.conf

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params

USER root

# RUN chmod +x /etc/nginx/

RUN mkdir -p /vol/static
RUN chmod 755 /vol/static

USER nginx