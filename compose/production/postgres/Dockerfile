FROM postgis/postgis:14-3.3

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance

COPY ./compose/production/postgres/initdb-postgis.sh /docker-entrypoint-initdb.d/10_postgis.sh
