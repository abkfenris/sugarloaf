import os

from sugarloaf import create_app
from sugarloaf.tasks import celery

env = os.environ.get('SUGARLOAF_ENV', 'dev')
app = create_app('sugarloaf.settings.%sConfig' % env.capitalize())

app.app_context().push()