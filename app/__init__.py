from flask import Flask

# http://flask.pocoo.org/docs/0.10/patterns/appfactories/


def create_app(config_filename):
    app = Flask(__name__, static_folder='templates/static')
    app.config.from_object(config_filename)

    # Init Flask-SQLAlchemy
    from app.basemodels import db
    db.init_app(app)

    from app.users.views import users
    app.register_blueprint(users, url_prefix='/api/v1/users')

    from app.baseviews import login_required, login1, mail
    from flask import render_template, send_from_directory
    import os

    # Init Flask-Mail
    mail.init_app(app)

    # Auth API
    app.register_blueprint(login1, url_prefix='/api/v1/')

    from app.roles.views import roles
    app.register_blueprint(roles, url_prefix='/api/v1/roles')

    # Blueprints
    from app.authors.views import authors
    app.register_blueprint(authors, url_prefix='/api/v1/authors')
    from app.comments.views import comments
    app.register_blueprint(comments, url_prefix='/api/v1/comments')
    from app.posts.views import posts
    app.register_blueprint(posts, url_prefix='/api/v1/posts')

    return app
