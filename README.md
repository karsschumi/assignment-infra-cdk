
# About the project project!

This project deploys a TO-DO python app with postgresql backend on AWS ECS. It contains the following stacks
* `Networking_stack` - Named as TodoozieNetworking, This will create the newtworking setup of a VPC, Subnets and realted network components
* `Ecr_stack` - Named as TodoozieEcr, This will create and ECR repository for storing docker images on AWS.
* `Fargate_Load_balancer_stack` - Named as TodoozieECSFargateLoadBalancer, This will create an Application loadbalancer, ECS cluster, tasks and service with scaling  configuration.

&nbsp;

# Built with
This project is mainly built with aws cdk - 2.25.0 and  python - 3.10.4</br>


&nbsp;

# Getting started
The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```


To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

Before running the below commands you need to setup aws credentials in your local machine. follow the below link
 https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

&nbsp;
# contributing
If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request to the main branch

&nbsp;

# Acknowledgement
https://aws.amazon.com/alb/ </br>
https://aws.amazon.com/iam/ </br>
https://aws.amazon.com/ecs/</br>
https://pypi.org/project/aws-cdk.core/

