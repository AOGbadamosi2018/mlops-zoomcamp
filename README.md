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