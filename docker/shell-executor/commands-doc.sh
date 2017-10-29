
# build Dockerfile:
docker build -t nishedcob/shell-executor .

# before first run, create a volume:
docker volume create --name code-shell-executor -o device=`pwd`/code -o o=bind

# to execute once the volume has been created:
docker run -it --user user --volume "code-shell-executor:/code" nishedcob/shell-executor
