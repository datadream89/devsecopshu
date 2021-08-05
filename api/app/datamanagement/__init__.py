

from flask import Flask

from datamanagement.configuration import key
from datamanagement.configuration import paths

from datamanagement.controllers.utils import regex_replace

from datamanagement.utils import one, pad, replaceNone

def create_app():
    app = Flask(__name__)
    app.jinja_env.filters['zip'] = zip
    app.jinja_env.filters['list'] = list
    app.jinja_env.filters['first_elem'] = one
    app.jinja_env.filters['regex_replace'] = regex_replace
    app.jinja_env.filters['pad'] = pad
    app.jinja_env.filters['replaceNone'] = replaceNone

    # Path and upload information
    app.config['UPLOAD_FOLDER'] = paths.UPLOAD_FOLDER
    app.config['EXAMPLES_FOLDER'] = paths.EXAMPLES_FOLDER
    app.secret_key = key.SECRET_KEY

    # from datamanagement.manageDB.routes import manageDB
    # from datamanagement.checkQuality.routes import qualityCheck
    from datamanagement.main.routes import main
    from datamanagement.pii.routes import pii
    from datamanagement.controllers.routes import controller
    # from datamanagement.data_lineage.routes import lineage
    # app.register_blueprint(manageDB)
    # app.register_blueprint(qualityCheck)
    app.register_blueprint(main)
    app.register_blueprint(pii)
    app.register_blueprint(controller)
    # app.register_blueprint(lineage)

    from datamanagement.angular_routes import angular_routes
    app.register_blueprint(angular_routes)

    return app
