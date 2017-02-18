import os
import logging

from sugarloaf import create_app

env = os.environ.get('SUGARLOAF_ENV', 'dev')
app = create_app('sugarloaf.settings.%sConfig' % env.capitalize())


@app.before_first_request
def setup_logging():
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)


if __name__ == '__main__':
    app.run()