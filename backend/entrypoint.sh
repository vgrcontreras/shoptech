#!/bin/bash

alembic upgrade head

python -m src.load