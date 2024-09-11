#!/usr/bin/env bash

cd "$(dirname "$0")"
amixer -M sset PCM 80%
amixer -M sset Mic 85%
. .venv/bin/activate
python record_greeting.py
