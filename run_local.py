# Run a test server.
from opl import oplMain #oplAPIApp
from flask_cors import CORS

oplAPIApp = oplMain.get_app()
cors = CORS(oplAPIApp, resources={r"/opl/*": {"origins": "*"}})
if __name__ == '__main__':
   oplMain.run(ssl_context="adhoc") # adhoc ssl enabled
   # oplMain.run()

# CORS added for local run
# gunicorn --bind 0.0.0.0:8080 run:oplAPIApp
