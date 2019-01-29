FROM microsoft/mssql-server-linux

# Create a config directory
RUN mkdir -p /usr/config

WORKDIR /usr/config

COPY . /usr/config

RUN chmod +x /usr/config/configure-db.sh
RUN chmod +x /usr/config/entrypoint.sh
RUN chmod +x /usr/config/wait-for-sqlserver.sh

EXPOSE 1433

CMD  exec /bin/bash entrypoint.sh
