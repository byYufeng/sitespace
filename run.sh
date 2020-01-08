#!/bin/bash
#Author: fsrm

gunicorn -w 2 -b 0.0.0.0:6080 index:app 1>logs/index.gunicorn.log 2>logs/index.gunicorn.err &
