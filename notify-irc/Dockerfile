FROM python:3.7.4-alpine3.10

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY entrypoint.sh notify_irc.py /

ENTRYPOINT ["/entrypoint.sh"]