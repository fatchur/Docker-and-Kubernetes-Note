## MYSQL DOCKER and DOCKER-COMPOSE NOTE

### Configure The DB and Table
- create `.sql` file for creating the table
- in Docker file:
- - add this for creating a DB `ENV MYSQL_DATABASE <db name>`
- copy your local `.sql` file to the `/docker-entrypoint-initdb.d/`, in Docker file: `COPY ./sql-scripts/ /docker-entrypoint-initdb.d/`
- To make the configuration running, you have to:
- - for usual docker: docker run -d -p <host port>:<docker port> --name <container name> -e MYSQL_ROOT_PASSWORD=<the pass> <image name>
- - for docker compose, add this to `.yml file`:    
`
environment:  
    MYSQL_ROOT_USER: root
    MYSQL_ROOT_PASSWORD: secret
    MYSQL_USER: root
    MYSQL_PASSWORD: secret
`