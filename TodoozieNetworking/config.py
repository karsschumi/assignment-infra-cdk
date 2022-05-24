from aws_cdk.aws_ec2 import RouterType
#networking configs
VPC_NAME = "Todoozie-VPC"
VPC_CIDR = "192.168.0.0/26"
VPC_MAX_AZ = 2
VPC_SUBNET_CIDR_MASK = 28
REGION = 'eu-central-1'
NUMBER_OF_NAT_GATEWAYS=2
PUBLIC_SUBNET_NAME="Public"
PRIVATE_SUBNET_NAME="Private"