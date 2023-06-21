from flask import Flask, request, jsonify,send_file
from flask_sqlalchemy import SQLAlchemy
import json
import zipfile
from werkzeug.security import check_password_hash, generate_password_hash
import os
import re
import requests
from flask_cors import CORS
import json
import zipfile
from flask import send_file
import io

app = Flask(__name__)
CORS(app)
CORS(app, origins='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
app.config['SQLALCHEMY_DATABASE_URI'] = ""
app.secret_key = os.environ.get("")
db = SQLAlchemy(app)

def validate_password(password):
    # Mínimo 8 caracteres.
    if len(password) < 8:
        return False
    # Mínimo 1 letra minúscula.
    if not re.search(r"[a-z]", password):
        return False
    # Mínimo 1 letra maiúscula.
    if not re.search(r"[A-Z]", password):
        return False
    # Mínimo 1 número.
    if not re.search(r"\d", password):
        return False
    return True

class User(db.Model):
    __tablename__ ="tb_usuario"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('recipes', lazy=True))
    image_url = db.Column(db.String)

    def __init__(self, title, ingredients, instructions, category, images=None):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions
        self.category = category
        self.images = images

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __init__(self, name):
        self.name = name

def buscar_imagens(query, access_key):
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1"
    headers = {"Authorization": f"Client-ID {access_key}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        image_urls = [result["urls"]["regular"] for result in results]
        return image_urls

    return []


@app.route('/')
def index():
    return jsonify({'message': 'Bem-vindo à API de drinks'})

@app.route("/login", methods=["POST"])
def login():    
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({
            "message": "Credenciais inválidas.",
            "statusCode": 401
        }), 401

    return jsonify({
        "message": "Login bem-sucedido!",
        "statusCode": 200
    }), 200

@app.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]

    if User.query.filter_by(email=email).first():
        return jsonify({
            "message": "Email já cadastrado.",
            "statusCode": 409
        }), 409

    """ if not validate_password(password):
        return jsonify({
            "message": "A senha não atende aos requisitos mínimos.",
            "statusCode": 400
        }), 400 """

    user = User()
    user.username = username
    user.password = generate_password_hash(password)
    user.email = email

    db.session.add(user)

    try:
        db.session.commit()  
        return jsonify({
                "message": "Cadastro bem-sucedido!",
                "statusCode": 201
            }), 201
    except Exception as error:
        print(error)
        return jsonify({
            "message": "Por algum motivo não conseguimos fazer o cadastro do usuário.",
            "statusCode": 500
        }), 500
        
@app.route('/resetPassword', methods=['PUT'])
def reset_password():
    email = request.json.get('email')
    password = request.json.get('password')

    # Verifique se o email existe no banco de dados
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({
            'message': 'Email não encontrado',
            'statusCode': 400
        }), 400

    # Atualize a senha do usuário
    user.password = generate_password_hash(password)
    db.session.commit()

    return jsonify({
        'message': 'Senha redefinida com sucesso',
        "statusCode": 200
        }), 200
 
@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if request.method == 'POST':
        title = request.json.get('title')
        ingredients = request.json.get('ingredients')
        instructions = request.json.get('instructions')
        category_id = request.json.get('category_id')

        category = Category.query.get(category_id)
        if not category:
            return jsonify({'message': 'Categoria não encontrada'}), 404

        recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, category=category)
        db.session.add(recipe)
        db.session.commit()

        # Buscar imagens relacionadas ao nome da receita
        images = buscar_imagens(title, 'TUuIA5-hqCaBz9cb9XAqd4hnyAjJHssTpxpz9XC7b8I')
        if images:
            recipe.image_url = images[0]  # Salvar a primeira URL de imagem encontrada

        db.session.commit()

        return jsonify({'message': 'Receita adicionada com sucesso'})
    else:
        recipes = Recipe.query.all()
        result = []
        for recipe in recipes:
            # Buscar imagens relacionadas ao nome da receita
            images = buscar_imagens(recipe.title, 'TUuIA5-hqCaBz9cb9XAqd4hnyAjJHssTpxpz9XC7b8I')
            image_url = images[0] if images else ''  # Obter a primeira URL de imagem encontrada ou uma string vazia se não houver imagens
            result.append({
                'id': recipe.id,
                'title': recipe.title,
                'ingredients': recipe.ingredients.split('\n'),
                'instructions': recipe.instructions,
                'category': {
                    'id': recipe.category.id,
                    'name': recipe.category.name
                },
                'image_url': image_url
            })
        return jsonify(result)
    
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    result = []
    for category in categories:
        result.append({
            'id': category.id,
            'name': category.name
        })
    return jsonify(result)

@app.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get_or_404(id)
    name = request.json.get('name')

    category.name = name
    db.session.commit()

    return jsonify({'message': 'Categoria atualizada com sucesso'})

@app.route('/categories', methods=['POST'])
def create_category():
    name = request.json.get('name')

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Categoria criada com sucesso'}), 201

@app.route('/recipes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': recipe.id,
            'title': recipe.title,
            'ingredients': recipe.ingredients.split('\n'),
            'instructions': recipe.instructions,
            'category': {
                'id': recipe.category.id,
                'name': recipe.category.name
            },
            'images': recipe.images.split('\n') if recipe.images else []
        })
    elif request.method == 'PUT':
        title = request.json.get('title')
        ingredients = request.json.get('ingredients')
        instructions = request.json.get('instructions')
        category_id = request.json.get('category_id')

        category = Category.query.get(category_id)
        if not category:
            return jsonify({'message': 'Categoria não encontrada'}), 404

        images = []
        for ingredient in ingredients:
            ingredient_images = buscar_imagens(ingredient, 'TUuIA5-hqCaBz9cb9XAqd4hnyAjJHssTpxpz9XC7b8I')
            if ingredient_images:
                images.extend(ingredient_images)

        recipe.title = title
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        recipe.category = category
        recipe.images = "\n".join(images)  # Salvar as URLs das imagens separadas por quebra de linha
        db.session.commit()
        return jsonify({'message': 'Receita atualizada com sucesso'})
    elif request.method == 'DELETE':
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({'message': 'Receita removida com sucesso'})

@app.route('/recipes/export', methods=['GET'])
def export_recipes():
    recipes = Recipe.query.all()
    data = []
    for recipe in recipes:
        recipe_data = {
            'id': recipe.id,
            'title': recipe.title,
            'ingredients': recipe.ingredients.split('\n'),
            'instructions': recipe.instructions.split('\n'),
            'category': {
                'id': recipe.category.id,
                'name': recipe.category.name
            },
            'image_url': recipe.image_url or ''
        }
        data.append(recipe_data)

    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    with zipfile.ZipFile('recipes.zip', 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.write('recipes.json')

    # Enviar o arquivo ZIP como resposta para download
    return send_file('recipes.zip', mimetype='application/zip', as_attachment=True), 200

@app.route('/recipes/<int:id>/details', methods=['GET'])
def recipe_details(id):
    recipe = Recipe.query.get_or_404(id)
    return jsonify({
        'id': recipe.id,
        'title': recipe.title,
        'ingredients': recipe.ingredients.split('\n'),
        'instructions': recipe.instructions,
        'category': {
            'id': recipe.category.id,
            'name': recipe.category.name
        },
        'image_url': recipe.image_url
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
