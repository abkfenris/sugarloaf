from flask import Blueprint, jsonify
from sqlalchemy import JSON, func

from sugarloaf.models import db, TrailStatus, Trail, Area

api = Blueprint('api', __name__)

@api.route('/current')
def current():
    latest = db.session.scalar(func.MAX(TrailStatus.dt))

    trails = db.session.query(Trail.name, 
                              Trail.difficulty,
                              Area.name.label('area'), 
                              TrailStatus.open,
                              TrailStatus.groomed,
                              TrailStatus.snowmaking,
                              )\
                       .filter(TrailStatus.trail_id == Trail.id,
                               Area.id == Trail.area_id,
                               TrailStatus.dt == latest)

    return jsonify(
        {'trails': [{'name': trail.name,
                     'difficulty': trail.difficulty,
                     'area': trail.area,
                     'groomed': trail.groomed,
                     'snowmaking': trail.snowmaking,
                     'open': trail.open} for trail in trails]})
    