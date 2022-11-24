#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_example_stack.cdk_example_stack import CdkExampleStack


app = cdk.App()

# Modify list of Construct inside CdkExampleStack to adjust modules/components that you would like to try
example_stack = CdkExampleStack(app, "CDKExampleStack")

app.synth()
