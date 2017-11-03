
echo ""

whoami
echo "says hello world!"
echo "from Docker!"

echo ""

lsb_release -a
uname -a

echo ""

cat /etc/os-release
os_id=$(grep "^\(ID\|id\)=" /etc/os-release | awk -F= '{print $2}')
echo "Detected OS ID: $os_id"

echo ""

echo "Starting PostgreSQL Cluster..."
if [ "$os_id" = 'debian' ] ; then
    /usr/bin/pg_ctlcluster 9.6 main start && echo "Started cluster!" || echo "Failed to start cluster!";
else
    if [ "$os_id" = 'alpine' ] ; then
        mkdir -p /run/postgresql && chown -R postgres:postgres /run/postgresql && chmod 755 /run/postgresql && \
        mkdir -p /var/run/postgresql && chown -R postgres:postgres /var/run/postgresql && \
        chmod 2777 /var/run/postgresql && \
        su - postgres -c \
        "export PGDATA=/var/lib/postgresql/data && postgres &" && \
            echo "Started cluster!" || echo "Failed to start cluster!";
        sleep 5s;
    else
        echo "Unknown/Unsupported OS";
        exit 1;
    fi
    #sh
fi

echo ""

su - user -c "psql -U user userdb -f /code/init.sql"
su - user -c "psql -U user userdb -f /code/main.sql"
