from aws_cdk import (
    Stack,
    SecretValue,
    CfnOutput,
    aws_ec2 as ec2, 
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_rds as rds,
    aws_ecs_patterns as ecs_patterns
)
from constructs import Construct

class ECSFargateStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get existing VPC from VPC ID
        vpc = ec2.Vpc.from_lookup(self, "VPC",
            vpc_id = "vpc-XXXXXXX" # << customize VPC ID here
        )
        cluster = ecs.Cluster(self, "ECSFargate-Cluster", vpc=vpc)
        
        # Create RDS Aurora DB Cluster
        db_user = "root" #modify username here
        db_password = "examplepassword" #modify password here
        db_name = "sample_db" #modify database name here

        db_cluster = rds.DatabaseCluster(self, "Database",
            engine=rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_2_08_1),
            credentials=rds.Credentials.from_username(
                username=db_user, 
                password=SecretValue.unsafe_plain_text(db_password)),
            default_database_name=db_name,
            instance_props=rds.InstanceProps(
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
                vpc_subnets=ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                ),
                vpc=vpc
            )
        )
        
        # Create ECS Fargate Cluster
        ecr_repository = "sample_ecr_repo" #modify ECR repository here

        repository = ecr.Repository.from_repository_name(self, construct_id, ecr_repository)
        image = ecs.ContainerImage.from_ecr_repository(repository, "latest")
        load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "ExampleEcsFargateService",
            cluster=cluster,            # Required
            cpu=512,                    # Default is 256
            desired_count=2,            # Default is 1
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                container_name="ExampleEcsFargateService",
                environment= { 
                    "DB_HOST" : db_cluster.cluster_read_endpoint.hostname,
                    "DB_USERNAME" : db_user,
                    "DB_PASSWORD" : db_password
                },
                image=image, 
                container_port=8080),
            memory_limit_mib=2048,      # Default is 512
            public_load_balancer=False)  # Default is True
            
        load_balanced_fargate_service.target_group.configure_health_check(
            path="/" #modify healthcheck path here
        )
        db_cluster.connections.allow_default_port_from(load_balanced_fargate_service.service);
        
        CfnOutput(self, 'AuroraDB Read Endpoint', value=db_cluster.cluster_read_endpoint.hostname)
