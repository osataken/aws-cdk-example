from aws_cdk import (
    Stack,
    aws_ec2 as ec2, 
)
from constructs import Construct
from example_modules import (
    aurora_rds,
    ecs_fargate,
    vpc_subnet,
)

class CdkExampleStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = vpc_subnet.VpcSubnet(self, "VPCSubnet")

        db_env = { 
            "DB_NAME" : "sample_db",
            "DB_USERNAME" : "root",
            "DB_PASSWORD" : "labpassword"
        }
        aurora = aurora_rds.Aurora(self, "DBCluster", vpc=vpc.vpc, env=db_env)

        ecs_env = { 
            "DB_HOST" : aurora.db_cluster.cluster_read_endpoint.hostname,
            "DB_NAME" : db_env["DB_NAME"],
            "DB_USERNAME" : db_env["DB_USERNAME"],
            "DB_PASSWORD" : db_env["DB_PASSWORD"],
        }
        fargate_service = ecs_fargate.ECSFargate(self, "ECSFargate", vpc=vpc.vpc, env=ecs_env)

        aurora.db_cluster.connections.allow_default_port_from(fargate_service.fargate_service.service)