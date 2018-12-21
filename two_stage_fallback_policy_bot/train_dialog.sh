#!/usr/bin/env bash
python -m rasa_core.train \
    -d data/domain.yml \
    -s data/stories.md \
    -o models/dialogue \
    -c config/dialog_policy.yml
