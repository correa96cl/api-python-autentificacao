from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            print(current_user)
            return jsonify({"message":"Autentificacao realizada com sucesso"}), 200

    return jsonify({"message": "Credenciais invalidas"}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizada com sucesso!"})

@app.route('/user', methods=['POST'])
@login_required
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuario cadastrado com sucesso"})

    return jsonify({"message": "Dados Invalidos"}), 401

@app.route("/users", methods=['GET'])
def get_users():
    user_list = User.query.all()

    user_list = [task.to_dict() for task in user_list]
    print(user_list)

    output = {
        "users": user_list,
        "total_tasks": len(user_list)
    }
    return jsonify(output)

@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {"username": user.username}
    
    return jsonify({"message": "Usuario nao encontrado"})

@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if user and data.get("password"):
        user.password = data.get("password")
        return jsonify({"message": f"Usuario {user.username} atualizado com sucesso!"})
    return jsonify({"message": "Usuario nao encontrado"}), 404

#fazer um metodo pa
@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if id_user == current_user.id:
        return jsonify({"message": "Delacao nao permitida"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuario {id_user} deletado com sucesso"})
    
    return jsonify({"message": "Usuario nao encontrado"}), 404

#fazer 

if __name__ == '__main__':
    app.run(debug=True)