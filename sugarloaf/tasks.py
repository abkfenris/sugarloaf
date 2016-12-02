import html2text
from celery import Celery
from flask import current_app
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from sugarloaf.settings import Config
from sugarloaf.models import db, TrailStatus, LiftStatus, Lift, SnowReporter, DailyReport
from sugarloaf.helpers.db import get_or_create_trail, get_or_create
from sugarloaf.helpers.scrape_sugarloaf_lifts_trails import update_time, update_lifts, update_trails, make_soup
import sugarloaf.helpers.scrape_sugarloaf_report as report_helper


celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

TaskBase = celery.Task

class ContextTask(TaskBase):
    abstract = True

    def __call__(self, *args, **kwargs):
        with current_app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)

celery.Task = ContextTask



def update_trail(trail, time):
    """Update a single trail"""
    t = get_or_create_trail(db.session, trail['name'], trail['area'])

    status = get_or_create(db.session, TrailStatus,
                           dt=time, 
                           open=trail['open'], 
                           groomed=trail['groomed'], 
                           snowmaking=trail['snowmaking'], 
                           trail=t)



def update_lift(lift, time):
    """Update a single lift"""
    l = get_or_create(db.session, Lift, name=lift['name'])

    running, scheduled, hold = False, False, False
    if lift['status'] is 'open':
        running = True
    if lift['status'] is 'scheduled':
        scheduled = True
    if lift['status'] is 'hold':
        hold = True
    
    status = get_or_create(db.session, LiftStatus,
                           dt=time,
                           lift=l,
                           running=running,
                           scheduled=scheduled,
                           hold=hold)


def update_trails_lifts():
    """Generate dict for all trails and distribute to individual tasks"""
    soup = make_soup()
    trails = update_trails(soup)
    lifts = update_lifts(soup)
    time = update_time(soup)

    for trail in trails:
        update_trail(trail, time)
    
    for lift in lifts:
        update_lift(lift, time)


def update_report():
    """Update the daily report"""
    soup = report_helper.make_soup()
    time = report_helper.update_time(soup)
    reporter = report_helper.report_reporter(soup)
    html = report_helper.report_text(soup)
    markdown = html2text.html2text(html)

    if reporter:
        r = get_or_create(db.session, SnowReporter,
                          name=reporter)
        report = get_or_create(db.session, DailyReport,
                               dt=time,
                               reporter=r,
                               report=markdown)
    else:
        report = get_or_create(db.session, DailyReport,
                               dt=time,
                               report=markdown)


@celery.task
def regular_update():
    """Kick off our regularly scheduled update"""
    update_trails_lifts()
    update_report()


celery.conf.beat_schedule = {
    'regular-update-15-min': {
        'task': 'sugarloaf.tasks.regular_update',
        'schedule': crontab(minute='*/15')
    }
}