from unicodedata import name
from constructs import Construct, DependencyGroup
from . import config
from aws_cdk import (
    Duration,
    Fn,
    RemovalPolicy,
    Stack,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_logs as cw,
    aws_ecr as ecr,
    aws_ec2 as ec2,
)
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
        self.db_container_log_config=ecs.LogDriver.aws_logs(log_group=self.cw_log_group,stream_prefix=config.ECS_CW_LOG_DB_STREAM_PREFIX)
        
        #task role
        self.task_role= iam.Role(self,config.TASK_ROLE_NAME,
                    assumed_by= iam.ServicePrincipal(config.TASK_ROLE_SERVICE_PRINCIPAL)
        )
        self.task_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(config.TASK_ROLE_MANAGED_POLICY_NAME))

        #task execution role
        self.task_execution_role= iam.Role(self,config.TASK_EXECUTION_ROLE_NAME,
                    assumed_by= iam.ServicePrincipal(config.EXECUTION_ROLE_SERVICE_PRINCIPAL)
        )
        self.task_execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(config.EXECUTION_ROLE_MANAGED_POLICY_NAME_1))
        self.task_execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(config.EXECUTION_ROLE_MANAGED_POLICY_NAME_2))

        #fargate task definition
        self.fargate_task_definition = ecs.FargateTaskDefinition(self, "TaskDefinition",
            cpu=config.ECS_TASK_DEF_CPU,
            execution_role=self.task_execution_role,
            task_role=self.task_role
        )
        self.ecr_repo=ecr.Repository.from_repository_name(self,Fn.import_value("ecrreponame"),Fn.import_value("ecrreponame"))
        self.app_container_log_config=ecs.LogDriver.aws_logs(log_group=self.cw_log_group,stream_prefix=config.ECS_CW_LOG_APP_STREAM_PREFIX)
        
        #App Container
        self.fargate_task_definition.add_container("AppContainer",
            image=ecs.ContainerImage.from_ecr_repository(repository= self.ecr_repo,tag=config.ECR_IMAGE_TAG),
            essential=True,
            container_name=config.APP_CONTAINER_NAME,
            port_mappings=[ecs.PortMapping(container_port=config.APP_CONTAINER_PORT,host_port=config.APP_CONTAINER_HOST_PORT,protocol=ecs.Protocol.TCP)],
            environment= config.APP_CONTAINER_HEALTH_ENVIRONMENT_VARIABLES,
            logging= self.app_container_log_config,
            
        )
        #DB Container
        self.fargate_task_definition.add_container("DBContainer",
            image=ecs.ContainerImage.from_registry(config.DB_CONTAINER_IMAGE),
            essential=True,
            container_name=config.DB_CONTAINER_NAME,
            port_mappings=[ecs.PortMapping(container_port=config.DB_CONTAINER_PORT,host_port=config.DB_CONTAINER_HOST_PORT,protocol=ecs.Protocol.TCP)],
            environment=config.DB_CONTAINER_HEALTH_ENVIRONMENT_VARIABLES,
            logging= self.db_container_log_config,
            health_check=ecs.HealthCheck(command=config.DB_CONTAINER_HEALTH_CHECK_COMMAND,interval=config.DB_CONTAINER_HEALTH_CHECK_INTERVAL,timeout=config.DB_CONTAINER_HEALTH_CHECK_TIMEOUT,retries=config.DB_CONTAINER_HEALTH_RETRY)
        )
        
        private_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType(config.ALB_PRIVATE_SUBNET_STRING))

        self.lb_ecs_service=albfs(self,"albfs",cluster=self.cluster,memory_limit_mib=config.ECS_SERVICE_MEMORY,cpu=config.ECS_SERVICE_CPU,
                            task_definition=self.fargate_task_definition,health_check_grace_period=config.ECS_SERVICE_HEALTH_CHECK_GRACE_PERIOD
                            ,task_subnets=private_subnets,desired_count=config.ECS_SERVICE_DESIRED_COUNT,listener_port=config.ALB_LISTENER_PORT,public_load_balancer=True,)
        self.lb_ecs_service.target_group.configure_health_check(path=config.ALB_HEALTH_CHECK_PATH,port=config.ALB_HEALTH_CHECK_PORT,unhealthy_threshold_count=config.ALB_HEALTH_CHECK_UNHEALTHY_THRESHOLD_COUNT,interval=config.ALB_HEALTH_CHECK_INTERVAL)