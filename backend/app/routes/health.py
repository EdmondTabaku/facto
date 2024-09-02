from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__, url_prefix='/health')


@health_bp.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'UP'}), 200
