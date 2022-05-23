
from multiprocessing.connection import Listener
from select import select
import aws_cdk
from click import launch
from constructs import Construct, DependencyGroup
from . import config
from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    CfnOutput
)
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_iam as iam
from aws_cdk import aws_logs as cw
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ec2 as ec2
from  aws_cdk.aws_elasticloadbalancingv2 import ApplicationLoadBalancer as alb
from  aws_cdk.aws_elasticloadbalancingv2 import ApplicationTargetGroup as tg
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService as albfs

class TodoozieECSFargateAlbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,networking_stack,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #ecs cluster
        self.cluster = ecs.Cluster(self, config.CLUSTER_NAME,
                    vpc=networking_stack.vpc,container_insights=True,cluster_name=config.CLUSTER_NAME
                )
        #cw log group
        self.cw_log_group = cw.LogGroup(self,config.ECS_CW_LOG_GROUP_NAME,log_group_name=config.ECS_CW_LOG_GROUP_NAME,retention=cw.RetentionDays.ONE_DAY,removal_policy=RemovalPolicy.DESTROY)
        self.db_container_log_config=ecs.LogDriver.aws_logs(log_group=self.cw_log_group,stream_prefix="db-container-logs")
        
        #task role
        self.task_role= iam.Role(self,config.ECS_TASK_ROLE_NAME,
                    assumed_by= iam.ServicePrincipal("ecs-tasks.amazonaws.com")
        )
        self.task_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess"))
        #task execution role
        self.task_execution_role= iam.Role(self,config.ECS_TASK_EXECUTION_ROLE_NAME,
                    assumed_by= iam.ServicePrincipal("ecs-tasks.amazonaws.com")
        )
        self.task_execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess"))
        self.task_execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy"))

        #fargate task definition
        self.fargate_task_definition = ecs.FargateTaskDefinition(self, "TaskDef",
           # memoryLimitMiB=config.ECS_TASK_DEF_MEMORY,
            cpu=config.ECS_TASK_DEF_CPU,
            execution_role=self.task_execution_role,
            task_role=self.task_role
        )
        self.ecr_repo=ecr.Repository.from_repository_name(self,"todoozierepo",config.ECR_REPO_NAME)
        self.app_container_log_config=ecs.LogDriver.aws_logs(log_group=self.cw_log_group,stream_prefix="app-container-logs")
        self.fargate_task_definition.add_container("AppContainer",
            image=ecs.ContainerImage.from_ecr_repository(repository= self.ecr_repo,tag="latest"),
            essential=True,
            container_name="App",
            port_mappings=[ecs.PortMapping(container_port=8000,host_port=8000,protocol=ecs.Protocol.TCP)],
            environment={ "SECRET_KEY": "77b070105b32e1b78c3b16374702a634ca1349e966e2c9e4cede09154a0e048f", "DB_PASSWORD": "admin"},
            logging= self.app_container_log_config,
            
        )
        self.fargate_task_definition.add_container("DBContainer",
            image=ecs.ContainerImage.from_registry("postgres:13.6"),
            essential=True,
            container_name="DB",
            port_mappings=[ecs.PortMapping(container_port=5432,host_port=5432,protocol=ecs.Protocol.TCP)],
            environment={ "POSTGRES_PASSWORD": "admin", "POSTGRES_DB": "todoozie_db"},
            logging= self.db_container_log_config,
            health_check=ecs.HealthCheck(command=["CMD-SHELL", "pg_isready"],interval=Duration.seconds(20),timeout=Duration.seconds(5),retries=5)
        )
        
        private_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType('PRIVATE_WITH_NAT'))

        self.lb_ecs_service=albfs(self,"albfs",cluster=self.cluster,memory_limit_mib=1024,cpu=512,
                            task_definition=self.fargate_task_definition,health_check_grace_period=Duration.seconds(300)
                            ,task_subnets=private_subnets,desired_count=2,listener_port=80,public_load_balancer=True,)
        self.lb_ecs_service.target_group.configure_health_check(path="/docs",port="8000",unhealthy_threshold_count=10,interval=Duration.seconds(120))