import os
from dotenv import load_dotenv




basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))


#giving acces to project in any os
#base directory


class Config():
    """
    Set config variables for the flask app.
    using environment variables where avaialbe otherwise
    create the config variable if not done already
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or "HIT THE INTIAL DRIFT!"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEPLOY_DATABASE_URL") or 'sqlite:///' + os.path.join(basedir, 'app.db')
    FLASK_APP= os.environ.get('FLASK_APP')
    FLASK_ENV= os.environ.get('FLASK_ENV')
    SQLALCHEMY_TRACK_MODIFICATIONS = False