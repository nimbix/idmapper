FROM python:2-alpine

#VOLUME /home
VOLUME /tmp

RUN pip install utils db
RUN pip install web.py

COPY idmapper.py /usr/local/bin/idmapper.py
CMD [ "python", "/usr/local/bin/idmapper.py" ]

