#!/usr/bin/env bash
ps -fe|grep wsgi:app|grep -v grep|gawk '{print $2}'|xargs kill -9