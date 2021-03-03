from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    
    import flask_db
    flask_db.init_app(app)
    
    import storage_api
    app.register_blueprint(storage_api.bp)
    
    # test route
    @app.route('/')
    def home():
        return 'online'
    
    return app