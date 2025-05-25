from flask import Flask, request, jsonify, Blueprint,render_template
from routes.main_router import main_router
from database.db import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
import stripe
from flask_ngrok import run_with_ngrok
from dotenv import load_dotenv

app = Flask(__name__)
run_with_ngrok(app)


load_dotenv()
stripe.api_key = os.getenv('STRIPE_API_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


jwt = JWTManager(app)
migrate = Migrate(app,db)

db.init_app(app)
with app.app_context():
    db.create_all()

app.json.sort_keys = False
app.register_blueprint(main_router)




@app.route("/")
def index():
    return jsonify({"message": "server running...."}), 200


if __name__ == "__main__":
    app.run(debug=True)
