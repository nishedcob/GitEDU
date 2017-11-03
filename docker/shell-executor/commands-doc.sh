#! /usr/bin/head -n 2
# Execute this file with 'source commands-doc.sh'

# build Dockerfile:
#######################
# Debian Stretch
docker build -t nishedcob/shell-executor:debian-stretch debian/stretch/
# Alpine Linux 3.6
docker build -t nishedcob/shell-executor:alpine-3.6 alpine/3.6/

# before first run, create a volume:
docker volume create --name code-shell-executor -o device=`pwd`/code -o o=bind

# to execute once the volume has been created:
##################################################
# Debian Stretch
docker run -it --user user --volume "code-shell-executor:/code" nishedcob/shell-executor:debian-stretch
# Alpine Linux 3.6
docker run -it --user user --volume "code-shell-executor:/code" nishedcob/shell-executor:alpine-3.6
