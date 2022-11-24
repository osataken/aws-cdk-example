from aws_cdk import (
    aws_ec2 as ec2, 
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_ecs_patterns as ecs_patterns
)
from constructs import Construct

class ECSFargate(Construct):

    @property
    def fargate_service(self):
        return self._fargate_service

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, env: dict[str, str],**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get existing VPC from VPC ID
        # vpc = ec2.Vpc.from_lookup(self, "VPC",
        #    vpc_id = "vpc-XXXXXXX" # << customize VPC ID here
        #)
        cluster = ecs.Cluster(self, "ECSFargate-Cluster", vpc=vpc)
        
        # Uncomment to pull image from ECR
        # ecr_repository = "amazon/amazon-ecs-sample" #modify ECR repository here
        # repository = ecr.Repository.from_repository_name(self, construct_id, ecr_repository)
        # image = ecs.ContainerImage.from_ecr_repository(repository, "latest")
        
        image = ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
        
        # Create ECS Fargate Cluster
        self._fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "ExampleEcsFargateService",
            cluster=cluster,            # Required
            cpu=512,                    # Default is 256
            desired_count=2,            # Default is 1
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                container_name="ExampleEcsFargateService",
                environment= env,
                image=image, 
                container_port=80),
            memory_limit_mib=2048,      # Default is 512
            public_load_balancer=True)  # Default is True
            
        self._fargate_service.target_group.configure_health_check(
            path="/" #modify healthcheck path here
        )
