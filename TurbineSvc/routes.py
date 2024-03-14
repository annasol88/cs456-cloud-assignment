from http.client import UNSUPPORTED_MEDIA_TYPE
from flask import Blueprint, request, jsonify,make_response
from models import db
import models

turbines_bp = Blueprint('turbines', __name__, url_prefix='/turbines')
measurements_bp = Blueprint('measurements', __name__, url_prefix='/measurements')

@turbines_bp.route('/', methods=['GET', 'POST'])
def turbines():
    if request.method == 'GET':
        return jsonify([turbine.to_dict() for turbine in models.Turbine.query.all()])
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                turbine = models.Turbine(serial = data['serial'])
                db.session.add(turbine)
                db.session.commit()
        except TypeError:
            return make_response(jsonify("No JSON supplied."), 500)
        except KeyError:
            return make_response(jsonify("Missing JSON data."), 500)
        except Exception:
            return make_response(jsonify("Internal server error."), 500)
    return make_response(jsonify("Method not supported."), 404)


@turbines_bp.route('/<int:id>', methods=['GET', 'DELETE'])
def turbine(id):
    turbine = models.Turbine.query.filter_by(id=id).first()
    if turbine is None:
        return make_response(jsonify("Index not found."), 500)
    if request.method == 'GET':
        return jsonify(turbine.to_dict())
    if request.method == 'DELETE':
        try:
            db.session.delete(turbine)
            db.session.commit()
            return make_response(jsonify({}), 200)
        except Exception:
            return make_response(jsonify("Internal server error."), 500)
    return make_response(jsonify("Method not supported."), 404)


@measurements_bp.route('/', methods=['GET'])
def measurement(id):
    if request.method == 'GET':
        serial = request.args.get('serial')
        measurements = None
        if serial is None:
            measurements = models.Measurement.query.all()
            
        measurements = models.Measurement.query.filter_by(serial=serial).first()
        
        if measurements is None and serial is None:
            return make_response(jsonify("Measurement serial not found."), 500)
        return jsonify(measurements.to_dict())
    return make_response(jsonify("Method not supported."), 404)