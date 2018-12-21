#!/usr/bin/env bash

python -m rasa_core.evaluate \
	-d models/dialogue \
	-s data/stories.md \
	-o matrix.pdf