#!/bin/bash
yum update -y

cd /tmp/
echo current dir: `pwd`

echo 'Downloading my site...'
# Download Lab files from AWS or replace the url with a link to the source code of your preferred website
# PASTE YOUR OWN RESOURCES instead of {name-of-your-public-bucket} and {name-of-your-zipped-website}
wget https://{name-of-your-public-bucket}.s3.amazonaws.com/{name-of-your-zipped-website}.zip

echo 'Setup docker ...'
#install docker on EC2
amazon-linux-extras install docker

#create docker group and add your ec2-user to manage Docker as a non-root user
groupadd docker
usermod -aG docker $USER
# activate the changes to groups
newgrp docker

# start Docker service
service docker start

echo 'Create docker file...'

echo '
FROM centos:7
LABEL maintainer="Katerina Bosko"

RUN yum -y install httpd unzip

# copy over zip file from EC2 to Docker container root folder (NOTE: ADD works with zip, COPY not)
# PASTE YOUR OWN RESOURCES
ADD {name-of-your-zipped-website.zip} .

#unzip inside docker container
# PASTE YOUR OWN RESOURCES
RUN unzip {name-of-your-zipped-website.zip} -d /var/www/html/

EXPOSE 80

#start web server
CMD apachectl -D FOREGROUND
' > /tmp/Dockerfile

echo 'Build docker container...'
# PASTE YOUR OWN VARIABLES FOR HUB USER AND REPO NAME
docker build . -t {hub-user}/{repo-name}:latest

echo 'Run docker container...'
# PASTE YOUR OWN VARIABLES FOR HUB USER AND REPO NAME
docker run -p 80:80 -t {hub-user}/{repo-name}:latest
