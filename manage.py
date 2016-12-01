#!/usr/bin/env python

import os

from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from flask_migrate import Migrate, MigrateCommand
from sugarloaf import create_app
from sugarloaf.models import db, User, Trail, TrailStatus, Lift, LiftStatus, SnowReporter, Area, DailyReport

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('SUGARLOAF_ENV', 'dev')
app = create_app('sugarloaf.settings.%sConfig' % env.capitalize())

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db, User=User, 
                Trail=Trail, TrailStatus=TrailStatus, 
                Lift=Lift, LiftStatus=LiftStatus,
                Area=Area,
                SnowReporter=SnowReporter,
                DailyReport=DailyReport)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        your SQLAlchemy models
    """

    db.create_all()

if __name__ == "__main__":
    manager.run()
