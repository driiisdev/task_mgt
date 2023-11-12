import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from config import Config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if not app.debug:    
  if not os.path.exists('logs'):
    os.mkdir('logs')
  file_handler = RotatingFileHandler('logs/taskmgt.log', maxBytes=10240, backupCount=10)
  file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
  file_handler.setLevel(logging.INFO)
  app.logger.addHandler(file_handler)
  app.logger.setLevel(logging.INFO)
  app.logger.info('Microblog startup')

from app import routes, models

