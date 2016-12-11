from flask import Blueprint, jsonify
from sqlalchemy import JSON, func

from sugarloaf.models import db, TrailStatus, Trail, Area

api = Blueprint('api', __name__)

@api.route('/current')
def current():
    """Return a json with most recent trail and lift conditions and daily report"""
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


@api.route('/summary')
def summary():
    """ Return json with a summary of the trail status by update """
    conditions = db.session.query(TrailStatus.dt, 
                                  TrailStatus.open, 
                                  TrailStatus.groomed, 
                                  TrailStatus.snowmaking, 
                                  Trail.difficulty, 
                                  Area.name,
                                  func.count())\
                            .filter(TrailStatus.trail_id == Trail.id, Trail.area_id == Area.id)\
                            .group_by(TrailStatus.dt, 
                                      TrailStatus.open, 
                                      TrailStatus.groomed, 
                                      TrailStatus.snowmaking, 
                                      Trail.difficulty,
                                      Area.name)

    output = {'conditions': [{
            'datetime': condition.dt,
            'open': condition.open,
            'groomed': condition.groomed,
            'snowmaking': condition.snowmaking,
            'difficulty': condition.difficulty,
            'trail_count': condition[5],
            'area': condition.name
        } for condition in conditions]}

    print(output)
    return jsonify(output)
