Download and Run
==============

Download
--------------
	git clone https://github.com/mraswan/opl_microservice.git
	cd opl_microservice
	pip install -r requirements

Prerequisite (to Run)
--------------
- install needed modules
`` pip install -r requirements.txt``	
`` create a folder named db``
`` opl_data.db holds the database. sqlite3 db/opl_data.db``
`` run the commands in sql/opl_daanase_schema.sql in the db``	
Configuration (if you need to change)
--------------


Run
--------------
- Run for development using:
`` python run.py``

- Run Server using Gunicorn (@ port 5000).
`` gunicorn --bind 0.0.0.0:5000 run:oplAPIApp ``
    Before executing make sure you have instance folder at same level as run.py file.
    instance folder should have empty __init__.py file and a config.py file with any variables specific
    to your project (do not checkin in this file.

Run in Docker
--------------
Assumes that you have Docker Installed from here.
-	https://docs.docker.com/docker-for-mac/ (for mac)
-	https://docs.docker.com/docker-for-windows/ (for windows)

Instructions to build and run.
$ cd <BASE_GIT_PATH>/opl_microservice
$ docker build -t docker-image:opl_microservice .
$ docker run -e GUNICORN_WORKERS=4 -e GUNICORN_ACCESSLOG=- -p 5000:5000 docker-image:opl_microservice


Documentation Swagger
---------------------
- http://localhost:5000/ -> It redirect to the documentation URL
- http://localhost:5000/opl/doc/


