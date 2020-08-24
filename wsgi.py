# Run a test server.
from opl import oplMain #oplAPIApp
app = oplMain.get_app()
if __name__ == '__main__':
   oplMain.run()

# gunicorn --bind 0.0.0.0:8080 wsgi:app
