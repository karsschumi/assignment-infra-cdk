#!/usr/bin/env python3


import aws_cdk as cdk
from TodoozieEcr.todoozie_ecr_stack import TodoozieEcrStack
from TodoozieNetworking.todoozie_vpc_stack import TodoozieVPCStack
from TodoozieECSFargateLoadBalancer.todoozie_ecs_fargate_alb_stack import TodoozieECSFargateAlbStack
app = cdk.App()
vpcstack=TodoozieVPCStack(app, "TodoozieNetworking")
TodoozieEcrStack(app,"TodoozieEcr")
TodoozieECSFargateAlbStack(app,"TodoozieECSFargateLoadBalancer",networking_stack=vpcstack)
app.synth()
