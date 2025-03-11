from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import (
    create_access_token, 
    get_jwt_identity, 
    jwt_required, 
    JWTManager, 
    get_jwt
)
from datetime import timedelta

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

@app.route('/')  # Test
def hello_world():
    return render_template('accueil.html')

# Route de connexion qui génère un token JWT avec rôle
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # Simuler un utilisateur admin
    if username == "admin" and password == "admin":
        access_token = create_access_token(identity=username, additional_claims={"role": "admin"})
        return jsonify(access_token=access_token)

    # Simuler un utilisateur standard
    elif username == "user" and password == "user":
        access_token = create_access_token(identity=username, additional_claims={"role": "user"})
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

# Vérificateur de rôle personnalisé
def role_required(role):
    def decorator(fn):
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != role:
                return jsonify({"msg": "Accès interdit : rôle insuffisant"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Route protégée avec n'importe quel utilisateur authentifié
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Route accessible uniquement par les administrateurs
@app.route("/admin", methods=["GET"])
@role_required("admin")
def admin():
    return jsonify({"msg": "Bienvenue dans l'espace administrateur !"})

if __name__ == "__main__":
    app.run(debug=True)
