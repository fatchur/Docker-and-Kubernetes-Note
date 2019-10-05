## Redis Docker Note

![](assets/redis.png)

### How To Use
1. Install docker-ce [link](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
2. Download ready to deploy tesseract docker: `docker pull fatchur/redis1804:v0`
3. **NOTE**: This docker is working well for ubuntu 18.04 (bionic)
4. Run the downloaded docker image: `sudo docker run --name redis_deploy -d -p 6379:6379 <image name>:v0`
5. **NOTE**: Now your service is up
6. to stop your service: `sudo docker ps -a`, `sudo docker stop <redis container name>`
7. to restart your redis server: `sudo docker start <redis container name>`


### Opend The Redis DB
1. enter redis docker: `sudo docker exec -it redis_deploy /bin/bash`
2. get redis data keys: `redis-cli --scan --pattern '*'`


### Other commands
- install redis on ubuntu: `apt-get install redis server`
- start redis server: `service redis-server start`
- stop redis server: `service redis-server stop`
- restart redis server: `service redis-server restart`
- enter redis DB: `redis-server`
