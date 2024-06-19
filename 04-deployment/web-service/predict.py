import pickle 

from flask import Flask , request , jsonify


with open('/workspaces/mlops-zoomcamp/04-deployment/model.bin', 'rb') as f_in:
    (dv, model)  = pickle.load(f_in)


def predict(features) : 
    X = dv.transform(features)
    preds = model.predict(X)

    return preds


app = Flask('duration-prediction')

@app.route('/predict', methods =["POST"])
def pred_endpoint():
    ride = request.json()
    pred = predict(ride)

    result = {'duration' : pred} 

    return jsonify(result)

if __name__ == 'main': 
    app.run(debug = True , host = '0.0.0.0', port = 9696)

