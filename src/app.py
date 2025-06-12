#Este módulo inicia el servidor API, conecta la base de datos y define los endpoints.

import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite  # Se importan todos los modelos

# Inicializa la app Flask
app = Flask(__name__)
app.url_map.strict_slashes = False

# Configura la base de datos (PostgreSQL o SQLite por defecto)
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensiones
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Manejo de errores personalizados
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap para ver todos los endpoints disponibles
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Ejemplo básico (puedes borrarlo si quieres)
@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response"
    }
    return jsonify(response_body), 200

# Endpoints para People
@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    return jsonify([p.serialize() for p in people]), 200

@app.route('/person/<int:person_id>', methods=['GET'])
def get_one_person(person_id):
    person = People.query.get(person_id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404
    return jsonify(person.serialize()), 200

# Endpoint crear person
@app.route('/people', methods=['POST'])
def create_person():
    data = request.json
    name = data.get("name")
    hair_color = data.get("hair_color")
    eye_color = data.get("eye_color")

    if not name:
        return jsonify({"msg": "El nombre es obligatorio"}), 400

    new_person = People(name=name, hair_color=hair_color, eye_color=eye_color)
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 201

# Endpoint crear planeta
@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.json
    name = data.get("name")
    climate = data.get("climate")
    terrain = data.get("terrain")

    if not name:
        return jsonify({"msg": "El nombre es obligatorio"}), 400

    new_planet = Planet(name=name, climate=climate, terrain=terrain)
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201   

# Endpoints para Planets
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# Usuarios
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

# Favoritos del usuario
# (Simulación con user_id = 1)
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = User.query.get(1)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify([fav.serialize() for fav in user.favorites]), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    new_fav = Favorite(user_id=1, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Planet added to favorites"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    new_fav = Favorite(user_id=1, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Person added to favorites"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    fav = Favorite.query.filter_by(user_id=1, planet_id=planet_id).first()
    if not fav:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Planet favorite deleted"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    fav = Favorite.query.filter_by(user_id=1, people_id=people_id).first()
    if not fav:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Person favorite deleted"}), 200

# Inicia el servidor
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)