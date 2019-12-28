#!/usr/bin/env bash
gunicorn -c start_app.py wsgi:app