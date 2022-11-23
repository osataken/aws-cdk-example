#!/usr/bin/env python3
import os

import aws_cdk as cdk

from ecs_fargate.ecs_fargate_stack import ECSFargateStack
from vpc_subnet.vpc_subnet_stack import VpcSubnetStack


app = cdk.App()

# Uncomment to try different example construct
vpc_stack = VpcSubnetStack(app, "VpcSubnetStack")
ecs_stack = ECSFargateStack(app, "ECSFargateStack", vpc=vpc_stack.vpc)

app.synth()
