from flask import Flask, render_template, jsonify, request, make_response
from flask_jwt_extended import (
    create_access_token, 
    get_jwt_identity, 
    jwt_required, 
    JWTManager,
    set_access_cookies,
    unset_jwt_cookies,
    get_jwt
)
from datetime import timedelta

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # Utilisation des Cookies pour le JWT
app.config["JWT_COOKIE_SECURE"] = False          # Mettre à True si en HTTPS
app.config["JWT_COOKIE_HTTPONLY"] = True         # Protection contre le JavaScript
app.config["JWT_COOKIE_SAMESITE"] = "Lax"        # Protéger contre les attaques CSRF
jwt = JWTManager(app)

@app.route('/')
def accueil():
    return render_template('formulaire.html')

# Route de connexion qui génère un token JWT et le stocke dans un Cookie
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Simulation d'authentification
    if username == "admin" and password == "admin":
        access_token = create_access_token(identity=username)
        response = make_response(jsonify({"msg": "Connexion réussie"}))
        set_access_cookies(response, access_token)  # Stocker le token dans un Cookie
        return response

    return jsonify({"msg": "Mauvais identifiant ou mot de passe"}), 401

# Route de déconnexion pour supprimer le Cookie
@app.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"msg": "Déconnexion réussie"}))
    unset_jwt_cookies(response)
    return response

# Route protégée nécessitant le Cookie JWT
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)
