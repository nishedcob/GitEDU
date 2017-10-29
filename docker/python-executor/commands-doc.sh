
# build Dockerfile:
#######################
# Debian Stretch
docker build -t nishedcob/python-executor:debian-stretch debian/stretch/
# Alpine Linux 3.6
docker build -t nishedcob/python-executor:alpine-3.6 alpine/3.6/

# before first run, create a volume:
docker volume create --name code-python-executor -o device=`pwd`/code -o o=bind

# to execute once the volume has been created:
##################################################
# Debian Stretch
docker run -it --user user --volume "code-python-executor:/code" nishedcob/python-executor:debian-stretch
# Alpine Linux 3.6
docker run -it --user user --volume "code-python-executor:/code" nishedcob/python-executor:alpine-3.6
