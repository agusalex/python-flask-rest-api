#!/bin/bash

flask db init
flask db migrate
python seed.py