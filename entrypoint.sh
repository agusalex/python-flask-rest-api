#!/bin/bash

flask db upgrade
exec gunicorn -b 0.0.0.0:$PORT "app:create_app()"
