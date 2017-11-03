
FROM registry.gitlab.com/nishedcob/gitedu/shell-executor:debian-stretch

RUN apt-get update && apt-get install -y postgresql postgresql-client

RUN echo "Starting PostgreSQL Cluster..." ; \
    /usr/bin/pg_ctlcluster 9.6 main start && echo "Started cluster!" || echo "Failed to start cluster!"; \
    su - postgres -c "createuser user && createdb -O user userdb"; \
    echo "Stopping PostgreSQL Cluster..." ; \
    /usr/bin/pg_ctlcluster 9.6 main stop && echo "Stopped cluster!" || echo "Failed to stop cluster!";

VOLUME ["/code"]
WORKDIR "/code"
