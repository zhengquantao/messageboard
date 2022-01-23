from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flasgger import Swagger

db = SQLAlchemy()

swagger = Swagger()

csrf = CSRFProtect()

redis = None


