#!/bin/bash

echo "Starting Granian Server!"
granian --interface=asgi --workers=8 --runtime-threads=2 --host=0.0.0.0 --port=8000 --factory app.asgi:create_app
