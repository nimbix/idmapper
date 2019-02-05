FROM python:2-alpine

RUN pip install --no-cache-dir utils db simplejson
RUN pip install --no-cache-dir web.py

COPY idmapper.py /usr/local/bin/idmapper.py
CMD [ "python", "/usr/local/bin/idmapper.py" ]

