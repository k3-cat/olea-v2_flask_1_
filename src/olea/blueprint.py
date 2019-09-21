from auth import auth_bp, views
from journal import journal_bp, views
from leaf import leaf_bp, views
from pink import pink_bp, views
from proj import proj_bp, views


def register_blueprints(app):
    '''Register Flask blueprints.'''
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(leaf_bp, url_prefix='/leaf')
    app.register_blueprint(pink_bp, url_prefix='/pink')
    app.register_blueprint(proj_bp, url_prefix='/proj')
    app.register_blueprint(journal_bp, url_prefix='/journal')


__all__ = ['views']
