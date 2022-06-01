from flask import render_template, request

from manager.extension import db
from manager.medical.controller import medicals
from manager.templates.index import indexs
from manager.manager_user.controller import managers
from manager.customer.controller import customers
from manager.bill.controller import bills
from manager.config import app
from manager.extension import db
from manager.postman import postmans


def create_app(config_file="config.py"):
    app.config.from_pyfile(config_file)
    db.create_all()
    app.register_blueprint(medicals)
    app.register_blueprint(indexs)
    app.register_blueprint(managers)
    app.register_blueprint(customers)
    app.register_blueprint(bills)
    app.register_blueprint(postmans)

    @app.errorhandler(404)
    def page_not_found(error):
        if 'x-access-token' in request.headers:
            return 'wrong url'
        return render_template('error_not_role.html')

    @app.errorhandler(400)
    def page_not_found(error):
        return 'bad request'

    @app.errorhandler(405)
    def page_not_found(error):
        return 'wrong methods'

    @app.errorhandler(500)
    def page_not_found(error):
        return 'sever error'

    return app
