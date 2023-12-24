from flask import jsonify, Blueprint, request, Response
import team85.controller.vehicle_type as vtc

vehicle_type_bp = Blueprint('vehicle_type', __name__)

@vehicle_type_bp.route('/', methods=['GET'])
def get_all_vehicle_types():
    all_types = vtc.get_vehicle_types()

    return jsonify(all_types)
