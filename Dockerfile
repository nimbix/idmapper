FROM python:3-alpine3.22

RUN pip install --no-cache-dir utils db simplejson
RUN pip install --no-cache-dir web.py

COPY idmapper.py /usr/local/bin/idmapper.py
CMD [ "python3", "/usr/local/bin/idmapper.py" ]

