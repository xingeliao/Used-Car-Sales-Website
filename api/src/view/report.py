from flask import jsonify, Blueprint, request
import team85.controller.report as rc


reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/seller-history', methods=['GET'])
def get_seller_history():
    history = rc.get_seller_history()
    return jsonify(history)


@reports_bp.route('/average-time-in-inventory', methods=['GET'])
def get_average_time_in_inventory():
    report = rc.get_average_time_in_inventory()
    return jsonify(report)


@reports_bp.route('/price-per-condition', methods=['GET'])
def get_price_per_condition():
    report = rc.get_price_per_condition()
    return jsonify(report)


@reports_bp.route('/parts-statistics', methods=['GET'])
def get_parts_statistics():
    report = rc.get_parts_statistics()
    return jsonify(report) 


@reports_bp.route('monthly-sales-summary', methods=['GET'])
def get_monthly_sales_summary():
    report = rc.get_monthly_sales_summary()
    return jsonify(report)


@reports_bp.route('monthly-sales-drilldown', methods=['GET'])
def get_monthly_sales_drilldown():
    params = request.args
    report = rc.get_monthly_sales_drilldown(**params)
    return jsonify(report)
    