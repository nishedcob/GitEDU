
FROM debian:stretch

ENV shell=/bin/sh
ENV user=user

# Greatly increases image size, optional:
#RUN apt-get update && apt-get install -y lsb-release

RUN apt-get update && apt-get install -y python3 python3-dev python3-pip virtualenv

RUN mkdir -p /code && echo "USER=$user" && echo "SHELL=$shell" && useradd -ms $shell $user && chown -v $user:$user /code
VOLUME ["/code"]
WORKDIR "/code"

ENTRYPOINT ["/bin/sh"]
CMD ["/code/exec.sh"]
