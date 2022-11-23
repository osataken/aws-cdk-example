from aws_cdk import (
    Stack,
    aws_ec2 as ec2, 
)
from constructs import Construct

class VpcSubnetStack(Stack):

    @property
    def vpc(self):
        return self._vpc

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_cidr = "10.0.0.0/16" # Modify CIDR here
        vpc_name = "myvpc" # Modify VPC Name here

        self._vpc = ec2.Vpc(self, "Vpc",
            vpc_name=vpc_name,
            ip_addresses=ec2.IpAddresses.cidr(vpc_cidr),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="private-",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="public-",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
            ],
        )