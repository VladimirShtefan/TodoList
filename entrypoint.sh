#!/bin/bash
python manage.py migrate --check
status=$?
if [[ $status != 0 ]]; then
  python manage.py migrate
fi
#openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -sha256 -days 365 \
#    -subj "/C=GB/ST=London/L=London/O=Alros/OU=IT Department/CN=localhost"
exec "$@"
