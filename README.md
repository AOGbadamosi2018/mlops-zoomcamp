# mlops-zoomcamp -- Deploying a model as a web-service 

* Creating a virtualenvironment with pipenv
* Creating a script with predictions 
* Putting the secript into a Flask App 
* Packaging the app to Docker

#### NOTES

To deploy the preictions as a web service
0.1 Convert the notebook to Py file. 
0.2 Create a Deployment folder , then create a webservice folder within that same folder. 
1. Scikit Learn Versions have to be the same when using scikit-learn 
2. Create a virtual environment using pipenv
3. Activate the environment using pipenv shell 
4. Create a prediction.py script that loads the models, transforms the features and routes the 
predictions call to a predict endpoint (using a flask decorator with the POST request option. )
5. Create a test .py file that contains a json payload to rest the file . 
6. Bind the prediction url to a WSGI server e.g a Gunicorn server using 
"gunicorn --bind=0.0.0.0:9696 predict:app"
If the port becomes taken use 
 - sudo netstat -tulnp to find the process id (usually ends in a /python) 
 - then sudo kill <process-id> to stop the process , then you can start the rebind. 
Or just restart the virtual environment. 
To selectively install dependencies in dev but not in production , we can use pipenv install --dev requests 



#HOW TO BUILD THE DOCKER FILE 


```bash
docker build -t ride-duration-prediction-service:v1 .
```



```bash 
docker run -it --rm -p 9696:9696 ride-duration-prediction-service:v1
```

#### The docker container can be deployed to AWS Beanstalk and or Kubernetes. 

#### precommit hooks
The precommit sample can be checked in the .git directory 
to add a standalone repo so that the hooks are local
use: 
1. git.init
2. Then within the standalone git repository we need to run 
    pre-commit sample-commit ? pre-commit-config.yaml
3. cd into git/hooks
4. Run pre-commit install 
5. We need to install the pre commit hook after creating the environemnt everytime we pull the repo 
6. we can use a gitignore to not commit pycache

#### infrastructre notes 
Create an infrastructure folder 
The terraform project takes at least on .tf file . 
locals variable is something used within a file 
variables are used across modules in a project and are usually required at runtime.

Then for each infrastructure create a relevant file for each service in a modules folder 
i.e ecr , s3 ,kinesis , maybe rds 

For help with resource configuration and properties look up https://developer.hashicorp.com/terraform?product_intent=terraform

To build the resources 
we can run terraform init from the project directory 

To install terraform on linux run 
1. curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add - (RESPONSE SHOULD BE -- OK)
2. sudo apt-add-repository "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
3. sudo apt update
4. sudo apt install terraform

terraform plan / terraform plan -var-file="vars/stg.tfvars"
terraform apply 
---------module.source_kinesis_stream.aws_kinesis_stream.stream: Creation complete after 31s [id=arn:aws:kinesis:eu-west-1:605272291968:stream/ride-prediction_mlops-zoomcamp]-----------------


Use terraform plan to view the actions taken when terraform apply is clicked.
-- Ensure to add kinesis full access to the IAM user

The state bucker is created manually and is used when we call terrafrom apply

Ensure to destroy the resources after the project is done 
Terraform expects bash style formatting for variables 


We generally prefer our datastreams and mlflow buckets be created before the ecr and lambda streams 

data streams ---> models_s3 ---> ecr ---> lambda

Needed to add the lambda-test code , the model code and then the Docker file to the tests directory 


Add the following inline policy to the IAM user 

{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"ecr:CreateRepository",
				"ecr:ReplicateImage",
				"ecr:DescribeRepositories",
				"ecr:ListTagsForResource",
				"ecr:DeleteRepository",
				"ecr:BatchCheckLayerAvailability",
				"ecr:CompleteLayerUpload",
				"ecr:GetDownloadUrlForLayer",
				"ecr:GetAuthorizationToken",
				"ecr:InitiateLayerUpload",
				"ecr:PutImage",
				"ecr:ListImages",
				"ecr:DescribeImages",
				"ecr:UploadLayerPart",
				"ecr:CompleteLayerUpload"
			],
			"Resource": "*"
		}
	]
}

CI/CD Pipelines are usually configured through Terraform 



FOR the IAM role of the lambda function , it is heavily dependency on the kinesis streams because it needs a separate iam role 
We configure the lambda to only be triggered when a new event arrives on the kinesis source stream 

Terrafrom issues and reinitialization notes 
EXPERIENCING ISSUES CONFIGURING CREATE FUNCTION ON LAMBDA BECAUSE IT CANNOT RECOGNISE THE ECR IMAGE. !!!!!!!!!!!!!!

POSTPONING STREAMING - KINESIS STREAMS  ALREADY COST $5 running for less than 2 days 

REMEMBER TO REINSTALL TERRAFORM DELETED THE AWS PLUGINS FROM HASHICORP

image uri - "605272291968.dkr.ecr.eu-west-1.amazonaws.com/stg_stream_model_duration.mlops-zoomcamp-abiodun.latest"


starting the mlflow tracking server 
mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://mlflow:vc7giErv1DVCyk60F22f@mlflow-backend-db.ct8mgeis0gmy.eu-west-1.rds.amazonaws.com:5432/postgres --default-artifact-root s3://mlflow-abiodung