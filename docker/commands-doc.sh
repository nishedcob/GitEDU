
# to execute when images should be updated remotely:
########################################################
# Login:
docker login registry.gitlab.com
# Debian Stretch
##################
# Build with correct remote tag:
docker build -t registry.gitlab.com/nishedcob/gitedu/shell-executor:debian-stretch shell-executor/debian/stretch/
docker build -t registry.gitlab.com/nishedcob/gitedu/python3-executor:debian-stretch python3-executor/debian/stretch/
# Push to remote registry with correct remote tag:
docker push registry.gitlab.com/nishedcob/gitedu/shell-executor:debian-stretch
docker push registry.gitlab.com/nishedcob/gitedu/python3-executor:debian-stretch
# Alpine 3.6
##############
# Build with correct remote tag:
docker build -t registry.gitlab.com/nishedcob/gitedu/shell-executor:alpine-3.6 shell-executor/alpine/3.6/
docker build -t registry.gitlab.com/nishedcob/gitedu/python3-executor:alpine-3.6 python3-executor/alpine/3.6/
# Push to remote registry with correct remote tag:
docker push registry.gitlab.com/nishedcob/gitedu/shell-executor:alpine-3.6
docker push registry.gitlab.com/nishedcob/gitedu/python3-executor:alpine-3.6
