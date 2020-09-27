#!/bin/bash

mkdir /logs

touch /logs/weibo_filter.err.log && touch /logs/weibo_filter.out.log

# python gateway.py
/usr/bin/supervisord
