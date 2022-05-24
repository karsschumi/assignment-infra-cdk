from constructs import Construct
from . import config
from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
    aws_ec2 as ec2
)


class TodoozieVPCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, config.VPC_NAME,
                           max_azs=config.VPC_MAX_AZ,
                           cidr=config.VPC_CIDR,
                           # configuration will create 2 groups in 2 AZs = 4 subnets.
                           subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name=config.PUBLIC_SUBNET_NAME,
                               cidr_mask=config.VPC_SUBNET_CIDR_MASK
                           ),
                           ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                               name=config.PRIVATE_SUBNET_NAME,
                               cidr_mask=config.VPC_SUBNET_CIDR_MASK
                           )
                           ],
                           nat_gateways=config.NUMBER_OF_NAT_GATEWAYS,
                           )
        CfnOutput(self, "vpcid",
                       value=self.vpc.vpc_id,export_name="vpcid")
