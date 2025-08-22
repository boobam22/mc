#!/bin/sh

VENV="$HOME/.venv"
HTTPX="$VENV/mc-httpx"

if [ ! -d "$HTTPX" ]; then
    mkdir -p $VENV

    python3 -m venv $HTTPX
    . $HTTPX/bin/activate
    pip install httpx h2
fi

mkdir -p ~/.local/bin
python3 -m zipapp src -p $HTTPX/bin/python -o ~/.local/bin/mc
