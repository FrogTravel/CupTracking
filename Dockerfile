FROM python:3.7

RUN mkdir -p /var/docker-tracking

WORKDIR /var/docker-tracking

COPY ./ /var/docker-tracking

RUN pip3 install opencv-python

RUN pip3 install flask

CMD ["python", "./script1.py"]

CMD ["python", "./web/web_service.py"]