#!/bin/sh
gunicorn main:adv -b 0.0.0.0:5001  --workers=3 --capture-output

#--forwarded-allow-ips="*"