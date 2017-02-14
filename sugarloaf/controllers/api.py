from flask import Blueprint, jsonify
import markdown
from sqlalchemy import func

from sugarloaf.models import db, TrailStatus, Trail, Area, Lift, LiftStatus, DailyReport

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
    lifts = db.session.query(Lift.name,
                             LiftStatus.running,
                             LiftStatus.scheduled,
                             LiftStatus.hold)\
                      .filter(LiftStatus.lift_id == Lift.id,
                              LiftStatus.dt == latest)
    latest_report = DailyReport.query.order_by(DailyReport.dt.desc()).first()

    return jsonify(
        {'trails': [{'name': trail.name,
                     'difficulty': trail.difficulty,
                     'area': trail.area,
                     'groomed': trail.groomed,
                     'snowmaking': trail.snowmaking,
                     'open': trail.open} for trail in trails],
        'datetime': latest,
        'report': markdown.markdown(latest_report.report),
        'lifts': [{'name': lift.name,
                   'running': lift.running,
                   'scheduled': lift.scheduled,
                   'hold': lift.hold} for lift in lifts]
        })


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
            'datetime': condition.dt.isoformat(),
            'open': condition.open,
            'groomed': condition.groomed,
            'snowmaking': condition.snowmaking,
            'difficulty': condition.difficulty,
            'trail_count': condition[6],
            'area': condition.name
        } for condition in conditions]}

    print(output)
    return jsonify(output)
