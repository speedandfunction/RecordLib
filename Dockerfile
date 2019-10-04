FROM python:3.7-stretch

COPY setup.py Pipfile Pipfile.lock /srv/

COPY nginx.conf /etc/nginx

WORKDIR /srv

COPY ./backend /srv/backend
COPY ./RecordLib /srv/RecordLib

RUN pip install pipenv && pipenv install --system && apt update && \
    apt install -y poppler-utils nginx && \
    useradd -ms /bin/bash gunicorn 

#COPY ./frontend/build /var/www/html


#USER gunicorn

EXPOSE 8000

COPY ./entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]

#ENTRYPOINT ["/usr/local/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--access-logfile", "wsgi:application"]