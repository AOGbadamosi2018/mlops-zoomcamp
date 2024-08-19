#import pickle
import mlflow 
import pickle
from mlflow.tracking import MlflowClient # for downloading the dict vectorizer artifacts  

from flask import Flask , request , jsonify

#using mlflow to get the model and artifacts instead 
#need to set up the mlfow server from the official docker image
RUN_ID = '8935c4ccc9f142aaa3b7f1f074feda2e'
MLFLOW_TRACKING_URI = 'http://3.253.72.252:5000'


mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient(tracking_uri =MLFLOW_TRACKING_URI)
logged_model = f'runs:/{RUN_ID}/model'

#better to point to the s3 location of the model incase the server goes down
logged_model = f's3://mlflow-abiodun/4/{RUN_ID}/artifacts/model'

model = mlflow.pyfunc.load_model(logged_model)

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    preds = model.predict(features)
    return float(preds[0])


app = Flask('duration-prediction')

@app.route('/predict', methods =["POST"])
def pred_endpoint():
    ride = request.get_json()
    pred = predict(ride)
 
    result = {'duration' : pred} 

    return jsonify(result)

if  __name__ == '__main__': 
    app.run(debug = True , host = '127.0.0.2', port = 9696)

