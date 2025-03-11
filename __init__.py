from flask import Flask #t
from flask import render_template
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from datetime import timedelta  # Import pour définir la durée de validité du token

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Ma clé privée
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Expiration du token après 1h
jwt = JWTManager(app)

@app.route('/')  # Test
def hello_world():
    return render_template('accueil.html')

# Route de connexion qui génère un token JWT
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Route protégée par un jeton valide
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)
