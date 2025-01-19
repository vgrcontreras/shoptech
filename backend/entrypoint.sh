#!/bin/bash

poetry run alembic downgrade base

poetry run alembic upgrade head