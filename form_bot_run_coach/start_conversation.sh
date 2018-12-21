#!/usr/bin/env bash

python -m rasa_core.run \
	-d models/dialogue \
	-u models/nlu/default/current \
	--endpoints endpoints.yml \
	-vv