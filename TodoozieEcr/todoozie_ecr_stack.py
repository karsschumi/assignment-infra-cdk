from constructs import Construct
from . import config
from aws_cdk import (
    Duration,
    Stack,
    CfnOutput
)
import aws_cdk.aws_ecr as ecr

class TodoozieEcrStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ecr_repository = ecr.CfnRepository(self, config.ECR_REPO_NAME,
        image_scanning_configuration=ecr.CfnRepository.ImageScanningConfigurationProperty(
            scan_on_push=config.ECR_SCAN_ON_PUSH
        ),
        image_tag_mutability=config.ECR_TAG_MUTABILITY,
        repository_name=config.ECR_REPO_NAME
        )
        CfnOutput(self, "ecrreponame",
                       value=self.ecr_repository.repository_name,export_name="ecrreponame")
