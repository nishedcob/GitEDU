#!/usr/bin/env bash
HOST="0.0.0.0"
PORT_NUMBER="8000"
PIPENV_COMMAND="pipenv2" # Disable use of pipenv because
			 # it doesn't install some git
                         # based dependencies correctly?!?
ENV_COMMAND="/usr/bin/env"
DJANGO_COMMAND="python manage.py runserver $HOST:$PORT_NUMBER"
command -v $PIPENV_COMMAND
if [ $? -eq 0 ]; then
    PIPENV_COMMAND="$ENV_COMMAND $PIPENV_COMMAND"
    $PIPENV_COMMAND --venv
    if [ ! $? -eq 0 ]; then
        $PIPENV_COMMAND --three
    fi
    $PIPENV_COMMAND install
    $PIPENV_COMMAND run $DJANGO_COMMAND
else
    source activate.sh
    $DJANGO_COMMAND
    deactivate
fi
