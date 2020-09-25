FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY . /home/ubuntu/color-transfer/
ENV UWSGI_INI /home/ubuntu/color-transfer/config.ini
ENV STATIC_PATH /home/ubuntu/color-transfer/static
ENV LD_LIBRARY_PATH /home/ubuntu/color-transfer/lib
WORKDIR /home/ubuntu/color-transfer/
