from aws_cdk import (
    aws_ec2 as ec2, 
    aws_rds as rds,
    SecretValue,
    CfnOutput,
)
from constructs import Construct

class Aurora(Construct):

    @property
    def db_cluster(self):
        return self._db_cluster

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, env: dict[str, str], **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self._db_cluster = rds.DatabaseCluster(self, "Database",
            engine=rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_2_08_1),
            credentials=rds.Credentials.from_username(
                username=env["DB_USERNAME"], 
                password=SecretValue.unsafe_plain_text(env["DB_PASSWORD"])),
            default_database_name=env["DB_NAME"],
            instance_props=rds.InstanceProps(
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
                vpc_subnets=ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                ),
                vpc=vpc
            )
        )
        
        CfnOutput(self, 'AuroraDB Read Endpoint', value=self._db_cluster.cluster_read_endpoint.hostname)