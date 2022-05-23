#ecs configs
CLUSTER_NAME = "Todoozie-cluster"
ECS_TASK_ROLE_NAME = "Todoozie-ecs-task-role"
ECS_TASK_EXECUTION_ROLE_NAME = "Todoozie-ecs-execution-role"
ECS_TASK_DEF_CPU = 256
ECS_TASK_DEF_MEMORY = 512

ECS_CW_LOG_GROUP_NAME="Todoozie-group"
ECR_REPO_NAME = "todoozierepo"
ECS_SERVICE_SG_NAME="todoozieecsservicesg"

ALB_LISTENER_NAME="todoozielistener"
ALB_LISTENER_PORT = 80