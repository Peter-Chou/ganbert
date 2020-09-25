#!/bin/bash

mkdir /logs

touch /logs/weibo_filter.err.log && touch /logs/weibo_filter.out.log

/usr/bin/supervisord
