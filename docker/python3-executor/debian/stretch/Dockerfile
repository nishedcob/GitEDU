
FROM registry.gitlab.com/nishedcob/gitedu/shell-executor:debian-stretch

RUN apt-get update && apt-get install -y python3 python3-dev python3-pip virtualenv

VOLUME ["/code"]
WORKDIR "/code"
