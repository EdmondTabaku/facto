from flask import Blueprint
from flask import request, jsonify
from app.services.prediction_service import predict

prediction_bp = Blueprint('prediction', __name__, url_prefix='/prediction')


@prediction_bp.route('/', methods=['POST'])
def predict_route():
    # Get the data from the POST request
    data = request.get_json(force=True)

    # Assuming data is a dictionary with a key 'text' containing the text to predict
    text = data['text']
    fake, confidence = predict(text)

    # Return the prediction as a JSON response
    return jsonify({'text': text,'fake': fake, 'confidence': confidence})
