from flask import Flask
from flask_cors import CORS
from apis import blueprint as api_blueprint
from apis import api
from tahelka.analytics.recorder import Recorder

app = Flask(__name__)
CORS(app)

# Read config
app.config.from_pyfile('config.py')

# Register blueprint
app.register_blueprint(api_blueprint)

# Register app error handlers
@app.errorhandler(404)
def handle_not_found(error):
    # Analytics
    status_code = 404
    Recorder(None, 'not_found_error', status_code).recordUsage()

    response = {"message": "Resource not found."}
    return response, status_code

@app.errorhandler(Exception)
def handle_internal_server_error(error):
    # Analytics
    status_code = 500
    Recorder(None, 'internal_server_error', status_code).recordUsage()

    print(error.__class__)
    print(error)

    response = {"message": "Internal server error."}
    return response, status_code

# Run
app.run(debug=True)
