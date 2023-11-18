from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///zindua.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://zindua_fylc_user:pNsCazyNi8VaZr6WwC4KQqBXoTbeRULs@dpg-clcaabjmot1c73dedc0g-a.oregon-postgres.render.com/zindua_fylc"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'secret_key'

app.json.compact = False

db = SQLAlchemy()
migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
