import db

from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = db.get_db()
        
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(flask_app):
    flask_app.teardown_appcontext(close_db)
    
def query_file_path(alias: str):
    return db._query_file_path(get_db(), alias)

def update_file_path(alias: str, path: str):
    return db._update_file_path(get_db(), alias, path)