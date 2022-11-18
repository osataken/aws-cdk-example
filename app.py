#!/usr/bin/env python3
import os

import aws_cdk as cdk

from ecs_fargate import ECSFargateStack


app = cdk.App()

# Uncomment to try different example construct
# ECSFargateStack(app, "ECSFargateStack")

app.synth()
