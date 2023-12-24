from flask import jsonify, Blueprint, request, Response
import team85.controller.manufacturer as mc

manu_bp = Blueprint('vehiclemanufacturer', __name__)

@manu_bp.route('/', methods=['GET'])
def get_types():
    response = mc.get_manufacturers()
    
    return jsonify(response)
