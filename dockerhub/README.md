## DOCKERHUB NOTE

### Push the Image to the Dockerhub
- login to your dockerhub account first </br>
`sudo docker login docker.io`

- tag your local image to your repository </br>
`sudo docker tag <image name>:<tag> <repository name>:tag`

- push your docker image
`sudo docker push <repository name>:<tag>`


### Pull the Image from Dockerhub
`sudo docker pull <repository name>`

