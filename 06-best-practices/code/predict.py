import pickle

from flask import Flask, jsonify, request

# using flask with open('/workspaces/mlops-zoomcamp/04-deployment/model.bin', 'rb') as f_in:
with open('model.bin', 'rb') as f_in:
    (dv, model) = pickle.load(f_in)


def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)

    return preds[0]


app = Flask('duration-prediction')


@app.route('/predict', methods=["POST"])
def pred_endpoint():
    ride = request.get_json()
    pred = predict(ride)

    result = {'duration': pred}

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.2', port=9696)
