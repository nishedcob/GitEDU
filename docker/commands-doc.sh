#! /usr/bin/head -n 2
# Execute this file with 'source commands-doc.sh'

# Execute other commands-doc.sh recursively...
for dir in `find . -type d | sed 's/^\.\///; /\//d; /^\.$/d'`; do
    echo $dir;
    cd $dir
    source ./commands-doc.sh
    cd ..
done

# to execute when images should be updated remotely:
########################################################
# Login:
docker login registry.gitlab.com
# Debian Stretch
##################
# Build with correct remote tag:
docker build -t registry.gitlab.com/nishedcob/gitedu/shell-executor:debian-stretch shell-executor/debian/stretch/
docker build -t registry.gitlab.com/nishedcob/gitedu/python3-executor:debian-stretch python3-executor/debian/stretch/
docker build -t registry.gitlab.com/nishedcob/gitedu/postgresql-executor:debian-stretch postgresql-executor/debian/stretch/
# Push to remote registry with correct remote tag:
docker push registry.gitlab.com/nishedcob/gitedu/shell-executor:debian-stretch
docker push registry.gitlab.com/nishedcob/gitedu/python3-executor:debian-stretch
docker push registry.gitlab.com/nishedcob/gitedu/postgresql-executor:debian-stretch
# Alpine 3.6
##############
# Build with correct remote tag:
docker build -t registry.gitlab.com/nishedcob/gitedu/shell-executor:alpine-3.6 shell-executor/alpine/3.6/
docker build -t registry.gitlab.com/nishedcob/gitedu/python3-executor:alpine-3.6 python3-executor/alpine/3.6/
docker build -t registry.gitlab.com/nishedcob/gitedu/postgresql-executor:alpine-3.6 postgresql-executor/alpine/3.6/
# Push to remote registry with correct remote tag:
docker push registry.gitlab.com/nishedcob/gitedu/shell-executor:alpine-3.6
docker push registry.gitlab.com/nishedcob/gitedu/python3-executor:alpine-3.6
docker push registry.gitlab.com/nishedcob/gitedu/postgresql-executor:alpine-3.6
