  File structure
  /ARVAGHDRAFT 
        /run.py  (contains the actual python code that will import the app and start the development server) ie. entry point to Flask app
        /config.py (stores configurations for the app) 
        /arvaghdraft  (Package which contains the flask application)
            /__init__.py (initializes application creating a Flask app instance. A contructor that pulls all of the parts of our application together into a package and then tells Python to treat it as a package)
            /views.py  (where routes are defined)
            /models.py  (define models for the application)
            /static/  ( contains static files i.e. CSS, Javascript, images)
                /main.css
            /templates/  (this is where html templates are stored)
                /base.html  
        /requirements.txt  (stores the package dependencies)
        /.flaskenv (set up flask env var)
        /.env (hide sensitive info)
        /venv
        Church source: (https://www.anglocelt.ie/2019/06/15/celebrating-two-centuries-of-worship-in-arva/)
