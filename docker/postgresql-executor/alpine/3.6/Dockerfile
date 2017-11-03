
FROM registry.gitlab.com/nishedcob/gitedu/shell-executor:alpine-3.6

RUN apk update && apk add postgresql && su - postgres -c "export PGDATA=/var/lib/postgresql/data && initdb"

RUN echo "Starting PostgreSQL Cluster..." ; \
    mkdir -p /run/postgresql && chown -R postgres:postgres /run/postgresql && chmod 755 /run/postgresql && \
    mkdir -p /var/run/postgresql && chown -R postgres:postgres /var/run/postgresql && \
    chmod 2777 /var/run/postgresql && su - postgres -c "export PGDATA=/var/lib/postgresql/data && postgres &" && \
        echo "Started cluster!" || echo "Failed to start cluster!"; \
    sleep 5s && netstat -tupln && \
    su - postgres -c "createuser user && createdb -O user userdb"; \
    echo "Stopping PostgreSQL Cluster..." ; killall postgres && \
        echo "Stopped cluster!" || echo "Failed to stop cluster!";

VOLUME ["/code"]
WORKDIR "/code"
