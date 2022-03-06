# Docker Container on AWS EC2
containerized my personal website and run it on AWS EC2 instance

## Description
In this lab, I launch EC2 instance on configured infrastructure (see [Lab 2](https://github.com/k-bosko/AWS_EC2_instance)), install Docker on EC2,
create a custom Docker container - copy over an existing application, install and launch web server, build and tag the Docker image, run application from Docker container on EC2 instance,
push Docker container to Docker Hub.

## Usage
To create custom EC2 instance on configured infrastructure, run:
 ```
 python kbosko-lab3.py
 ```

While creating EC2 instance, the shell script `Docker.sh` is executed which installs Docker and Apache web server, creates Docker container, builds it and runs it. 

Docker container runs my website www.cross-validated.com which is downloaded from S3 bucket created in previous [Lab 2](https://github.com/k-bosko/AWS_EC2_instance).

NOTE: you need to paste your own resources both in python and bash scripts.

## Debugging 

There are several ways to debug if got stuck:

1.	Attach shell to docker container
```
#check docker ID
docker ps
docker exec -it {container ID} bash
```

2.	Check log file for EC2 instance through AWS management console

Right-click on EC2 instance --> Monitor and troubleshoot --> Get system log

3. Check log file for container after SSH into the instance from local machine

```
sudo less  /var/log/cloud-init-output.log
```

See documentation on how to [Run commands on your Linux instance at launch](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)

4. Check that UserData got attached to EC2 instance from AWS management console

Right-click on instance --> Instance Settings --> View/Change User Data

## Pushing Docker Container to Docker Hub

Pushing Docker container to repo in Docker Hub:

1.	Create repository in Docker Hub
2.	Docker login
3.	Retag your Docker container 

`docker tag <existing-image> <hub-user>/<repo-name>[:<tag>]`

or when building assign correct tags

`docker build -t <hub-user>/<repo-name>[:<tag>]`

4.	Docker push 

`docker push <hub-user>/<repo-name>:<tag>`

See documentation [here](https://docs.docker.com/docker-hub/repos/)

