from flask import Flask
from flask_cors import CORS
from apis import blueprint as api_blueprint
from apis import api

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

    response = {"message": "Resource not found."}
    return response, 404

@app.errorhandler(Exception)
def handle_internal_server_error(error):
    # Analytics
    print(error.__class__)
    print(error)

    response = {"message": "Internal server error."}
    return response, 500

# Run
app.run(debug=True)
