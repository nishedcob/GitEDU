
FROM alpine:3.6

ENV shell=/bin/sh
ENV user=user

RUN apk update && apk add python3 python3-dev py-virtualenv

RUN mkdir -p /code && echo "USER=$user" && echo "SHELL=$shell" && echo "SHELL is not used in this Dockerfile" &&\
    adduser -D $user && chown -v $user:$user /code
VOLUME ["/code"]
WORKDIR "/code"

ENTRYPOINT ["/bin/sh"]
CMD ["/code/exec.sh"]
