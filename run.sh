#!/usr/bin/env bash

cd "$(dirname "$0")"
. .venv/bin/activate
python guestbook.py
