FROM mysql

ENV MYSQL_DATABASE safety
COPY ./sql/ /docker-entrypoint-initdb.d/
EXPOSE 3306
WORKDIR /docker-entrypoint-initdb.d/

