#import pickle
import mlflow 
import mlflow.tracking impirt MlflowClient # for downloading the dict vectorizer artifacts  

from flask import Flask , request , jsonify

 
# # using flask with open('/workspaces/mlops-zoomcamp/04-deployment/model.bin', 'rb') as f_in:
# with open('model.bin', 'rb') as f_in:
#     (dv, model)  = pickle.load(f_in)

#using mlflow to get the model and artifacts instead 
#need to set up the mlfow server from the official docker image
RUN_ID = 'b43bca8aa8e46a6b8257fe4541b1136'
MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'

client = MlflowClient(tracking_uri =MLFLOW_TRACKING_URI)
logged_model = f'runs:/{RUN_ID}/model'

path = client.download_artifacts(run_id = RUN_ID, path = 'dict_vectorizer.bin')

print('downloding the dict vectorizer')
with open(path, 'rb') as f_out:
     dv = pickle.load(f_out)

logged_model = f'runs:/{RUN_ID}/model'

model = mlflow.pyfunc.load_model(logged_model)


def predict(features) : 
    X = dv.transform(features)
    preds = model.predict(X)

    return preds[0]


app = Flask('duration-prediction')

@app.route('/predict', methods =["POST"])
def pred_endpoint():
    ride = request.get_json()
    pred = predict(ride)
 
    result = {'duration' : pred} 

    return jsonify(result)

if  __name__ == '__main__': 
    app.run(debug = True , host = '127.0.0.2', port = 9696)

