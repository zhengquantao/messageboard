# from flask_swagger.swagger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()

# swagger = Swagger()

csrf = CSRFProtect()

redis = None


