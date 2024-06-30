# mlops-zoomcamp -- Deploying a model as a web-service 

* Creating a virtualenvironment with pipenv
* Creating a script with predictions 
* Putting the secript into a Flask App 
* Packaging the app to Docker



```bash
docker build -t ride-duration-prediction-service:v1 .
```



```bash 
docker run -it --rm -p 9696:9696 ride-duration-prediction-service:v1
```