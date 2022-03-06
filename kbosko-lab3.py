'''
Author: Katerina Bosko
CS6620 Lab3: launch EC2 instance on configured infrastructure (see Lab2), install Docker on EC2,
            create a custom Docker container - copy over an existing application, install and launch web server,
            build and tag the Docker image, run application from Docker container on EC2 instance

'''

import boto3
from botocore.exceptions import ClientError

AWS_REGION = 'us-east-1'

SUBNET_TAG_VALUE = 'cs6620-lab2-subnet'
ROUTE_TABLE_TAG_VALUE = 'cs6620-lab2-route-table'
SECURITY_GROUP_TAG_VALUE = 'cs6620-lab2-security-group'
INSTANCE_TAG_VALUE = 'lab3-Linux'

#Amazon Linux 2 AMI (HVM) - Kernel 5.10, SSD Volume Type
IMAGE_ID = 'ami-033b95fb8079dc481'
INSTANCE_TYPE = 't2.micro'

# PASTE YOUR KEY PAIR HERE
KEY_NAME = '{your-key-pair.pem}'
SCRIPT_TO_RUN_ON_EC2 = 'Docker.sh'


def get_custom_subnet_id(client):
    '''
    Searches for existing subnet on a given VPC based on its tag value
    If found, returns subnet id
    Else returns empty response object (i.e. False)
    '''
    try:
        response = client.describe_subnets(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        SUBNET_TAG_VALUE,
                    ]
                },
            ],
        )
        if response['Subnets']:
            subnet_id = response['Subnets'][0]['SubnetId']
            print(f'Custom subnet exists. ID={subnet_id}')
            return subnet_id
    except ClientError:
        print('Failed while searching for existing subnet')
        raise
    else:
        return response['Subnets']

def get_custom_security_group(client):
    '''
    Searches for existing security group on a given VPC based on its tag value
    If found, returns security group id
    Else returns empty response object (i.e. False)
    '''
    try:
        response = client.describe_security_groups(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        SECURITY_GROUP_TAG_VALUE,
                    ]
                },
            ],
        )
        if response['SecurityGroups']:
            security_group_id = response['SecurityGroups'][0]['GroupId']
            print(f'Custom security group exists. ID={security_group_id}')
            return security_group_id
    except ClientError:
        print('Failed while searching for existing security group')
        raise
    else:
        return response['SecurityGroups']

def get_custom_ec2_instance(client):
    '''
    Searches for existing EC2 instance based on the given tag
    Returns public IP address of the custom EC2 instance
    '''
    try:
        response = client.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        INSTANCE_TAG_VALUE,
                    ]
                },
            ],
        )
        if response['Reservations']:
            ec2_id = response['Reservations'][0]['Instances'][0]['InstanceId']
            print(f'Custom EC2 instance exists. ID={ec2_id}')
            ec2_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
            return ec2_ip
    except ClientError:
        print('Failed while searching for existing EC2 instance')
        raise

def create_custom_instance(resource, security_group_id, subnet_id):
    '''
    Creates custom EC2 instance with specified configurations
    '''
    try:
        with open('Docker.sh', 'r') as fp:
            script=fp.read()

        instance = resource.create_instances(
            ImageId = IMAGE_ID,
            MinCount = 1,
            MaxCount = 1,
            InstanceType = INSTANCE_TYPE,
            KeyName = KEY_NAME,
            UserData=script,
            NetworkInterfaces=[
                        {
                            'AssociatePublicIpAddress': True,
                            'DeleteOnTermination': True,
                            'DeviceIndex': 0,
                            'Groups': [
                                security_group_id,
                            ],
                            'SubnetId': subnet_id,
                        },
                    ],
            TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': INSTANCE_TAG_VALUE
                            },
                        ]
                    },
                ],
        )
        ec2_id = instance[0].id
        print(f'Created instance with ID: {ec2_id}')
    except ClientError:
        print('Failed to create custom EC2 instance')
        raise
    else:
        return ec2_id


def main():
    # create EC2 client and resource
    resource = boto3.resource('ec2', region_name=AWS_REGION)
    client = boto3.client('ec2', region_name=AWS_REGION)

    # create public subnet within VPC, if it doesn't exist already
    subnet_id = get_custom_subnet_id(client)
    security_group_id = get_custom_security_group(client)

    # create EC2 instance with given specifications
    ec2_id = get_custom_ec2_instance(client)
    if not ec2_id:
        ec2_id = create_custom_instance(resource, security_group_id, subnet_id)

    print(f"access application at: http://{ec2_id}")


if __name__ == '__main__':
    main()
